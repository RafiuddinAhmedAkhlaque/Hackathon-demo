package services

import (
	"fmt"
	"time"

	"github.com/ecommerce/payment-service/models"
	"github.com/ecommerce/payment-service/repositories"
	"github.com/ecommerce/payment-service/utils"
	"github.com/google/uuid"
)

type PaymentService struct {
	paymentRepo     *repositories.PaymentRepository
	transactionRepo *repositories.TransactionRepository
}

func NewPaymentService(paymentRepo *repositories.PaymentRepository, transactionRepo *repositories.TransactionRepository) *PaymentService {
	return &PaymentService{
		paymentRepo:     paymentRepo,
		transactionRepo: transactionRepo,
	}
}

func (s *PaymentService) CreatePayment(req models.CreatePaymentRequest) (*models.Payment, error) {
	if err := s.validateCreateRequest(req); err != nil {
		return nil, err
	}

	payment := &models.Payment{
		ID:          uuid.New().String(),
		OrderID:     req.OrderID,
		UserID:      req.UserID,
		Amount:      utils.RoundToDecimalPlaces(req.Amount, req.Currency),
		Currency:    req.Currency,
		Status:      models.PaymentStatusPending,
		MethodID:    req.MethodID,
		Description: req.Description,
		CreatedAt:   time.Now(),
		UpdatedAt:   time.Now(),
	}

	saved, err := s.paymentRepo.Save(payment)
	if err != nil {
		return nil, fmt.Errorf("failed to save payment: %w", err)
	}

	return saved, nil
}

func (s *PaymentService) ProcessPayment(paymentID string) (*models.Payment, error) {
	payment, err := s.paymentRepo.FindByID(paymentID)
	if err != nil {
		return nil, err
	}

	if payment.Status != models.PaymentStatusPending {
		return nil, fmt.Errorf("payment is not in pending status: %s", payment.Status)
	}

	// Simulate payment processing (always succeeds in this mock)
	payment.Status = models.PaymentStatusCompleted
	payment.UpdatedAt = time.Now()

	// Create charge transaction
	tx := &models.Transaction{
		ID:        uuid.New().String(),
		PaymentID: payment.ID,
		Type:      models.TransactionTypeCharge,
		Amount:    payment.Amount,
		Currency:  payment.Currency,
		Status:    "completed",
		Metadata: map[string]string{
			"order_id": payment.OrderID,
			"user_id":  payment.UserID,
		},
		CreatedAt: time.Now(),
	}

	payment.TransactionID = tx.ID
	s.transactionRepo.Save(tx)
	s.paymentRepo.Save(payment)

	return payment, nil
}

func (s *PaymentService) GetPayment(paymentID string) (*models.Payment, error) {
	return s.paymentRepo.FindByID(paymentID)
}

func (s *PaymentService) GetPaymentsByOrder(orderID string) ([]*models.Payment, error) {
	return s.paymentRepo.FindByOrderID(orderID)
}

func (s *PaymentService) GetPaymentsByUser(userID string) ([]*models.Payment, error) {
	return s.paymentRepo.FindByUserID(userID)
}

func (s *PaymentService) CancelPayment(paymentID string) (*models.Payment, error) {
	payment, err := s.paymentRepo.FindByID(paymentID)
	if err != nil {
		return nil, err
	}

	if payment.Status != models.PaymentStatusPending {
		return nil, fmt.Errorf("only pending payments can be cancelled")
	}

	payment.Status = models.PaymentStatusCancelled
	payment.UpdatedAt = time.Now()
	s.paymentRepo.Save(payment)

	return payment, nil
}

func (s *PaymentService) GetPaymentTotal(userID string) (float64, error) {
	payments, err := s.paymentRepo.FindByUserID(userID)
	if err != nil {
		return 0, err
	}

	var total float64
	for _, p := range payments {
		if p.Status == models.PaymentStatusCompleted {
			total += p.Amount
		}
	}
	return total, nil
}

func (s *PaymentService) validateCreateRequest(req models.CreatePaymentRequest) error {
	ve := utils.NewValidationErrors()
	ve.Add(utils.ValidateRequired(req.OrderID, "order_id"))
	ve.Add(utils.ValidateRequired(req.UserID, "user_id"))
	ve.Add(utils.ValidatePositiveAmount(req.Amount, "amount"))
	ve.Add(utils.ValidateCurrency(req.Currency))
	ve.Add(utils.ValidateRequired(req.MethodID, "method_id"))

	if ve.HasErrors() {
		return fmt.Errorf("validation failed: %s", ve.Error())
	}
	return nil
}

