package services

import (
	"fmt"
	"time"

	"github.com/ecommerce/payment-service/models"
	"github.com/ecommerce/payment-service/repositories"
	"github.com/ecommerce/payment-service/utils"
	"github.com/google/uuid"
)

type RefundService struct {
	paymentRepo     *repositories.PaymentRepository
	transactionRepo *repositories.TransactionRepository
}

func NewRefundService(paymentRepo *repositories.PaymentRepository, transactionRepo *repositories.TransactionRepository) *RefundService {
	return &RefundService{
		paymentRepo:     paymentRepo,
		transactionRepo: transactionRepo,
	}
}

func (s *RefundService) CreateRefund(req models.CreateRefundRequest) (*models.Refund, error) {
	if err := s.validateRefundRequest(req); err != nil {
		return nil, err
	}

	// Find the original payment
	payment, err := s.paymentRepo.FindByID(req.PaymentID)
	if err != nil {
		return nil, fmt.Errorf("payment not found: %s", req.PaymentID)
	}

	if payment.Status != models.PaymentStatusCompleted {
		return nil, fmt.Errorf("can only refund completed payments")
	}

	// Calculate total already refunded
	totalRefunded, err := s.getTotalRefunded(payment.ID)
	if err != nil {
		return nil, err
	}

	if totalRefunded+req.Amount > payment.Amount {
		return nil, fmt.Errorf("refund amount (%.2f) would exceed payment amount (%.2f), already refunded: %.2f",
			req.Amount, payment.Amount, totalRefunded)
	}

	// Create refund
	refund := &models.Refund{
		ID:        uuid.New().String(),
		PaymentID: req.PaymentID,
		Amount:    utils.RoundToDecimalPlaces(req.Amount, payment.Currency),
		Reason:    req.Reason,
		Status:    models.RefundStatusCompleted,
		CreatedAt: time.Now(),
	}

	// Create refund transaction
	tx := &models.Transaction{
		ID:        uuid.New().String(),
		PaymentID: payment.ID,
		Type:      models.TransactionTypeRefund,
		Amount:    refund.Amount,
		Currency:  payment.Currency,
		Status:    "completed",
		Metadata: map[string]string{
			"refund_id": refund.ID,
			"reason":    req.Reason,
		},
		CreatedAt: time.Now(),
	}

	s.transactionRepo.Save(tx)

	// Update payment status if fully refunded
	if totalRefunded+req.Amount >= payment.Amount {
		payment.Status = models.PaymentStatusRefunded
		payment.UpdatedAt = time.Now()
		s.paymentRepo.Save(payment)
	}

	return refund, nil
}

func (s *RefundService) GetRefundsForPayment(paymentID string) ([]*models.Transaction, error) {
	txs, err := s.transactionRepo.FindByPaymentID(paymentID)
	if err != nil {
		return nil, err
	}

	refunds := make([]*models.Transaction, 0)
	for _, tx := range txs {
		if tx.Type == models.TransactionTypeRefund {
			refunds = append(refunds, tx)
		}
	}
	return refunds, nil
}

func (s *RefundService) getTotalRefunded(paymentID string) (float64, error) {
	txs, err := s.transactionRepo.FindByPaymentID(paymentID)
	if err != nil {
		return 0, err
	}

	var total float64
	for _, tx := range txs {
		if tx.Type == models.TransactionTypeRefund {
			total += tx.Amount
		}
	}
	return total, nil
}

func (s *RefundService) validateRefundRequest(req models.CreateRefundRequest) error {
	ve := utils.NewValidationErrors()
	ve.Add(utils.ValidateRequired(req.PaymentID, "payment_id"))
	ve.Add(utils.ValidatePositiveAmount(req.Amount, "amount"))
	ve.Add(utils.ValidateRequired(req.Reason, "reason"))

	if ve.HasErrors() {
		return fmt.Errorf("validation failed: %s", ve.Error())
	}
	return nil
}

