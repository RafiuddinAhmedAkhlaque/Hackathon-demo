package services

import (
	"github.com/ecommerce/payment-service/models"
	"github.com/ecommerce/payment-service/repositories"
)

type LedgerSummary struct {
	TotalCharges    float64 `json:"total_charges"`
	TotalRefunds    float64 `json:"total_refunds"`
	NetRevenue      float64 `json:"net_revenue"`
	ChargeCount     int     `json:"charge_count"`
	RefundCount     int     `json:"refund_count"`
	TransactionCount int    `json:"transaction_count"`
}

type LedgerService struct {
	transactionRepo *repositories.TransactionRepository
}

func NewLedgerService(transactionRepo *repositories.TransactionRepository) *LedgerService {
	return &LedgerService{
		transactionRepo: transactionRepo,
	}
}

func (s *LedgerService) GetSummary() (*LedgerSummary, error) {
	totalCharges, err := s.transactionRepo.GetTotalByType(models.TransactionTypeCharge)
	if err != nil {
		return nil, err
	}

	totalRefunds, err := s.transactionRepo.GetTotalByType(models.TransactionTypeRefund)
	if err != nil {
		return nil, err
	}

	return &LedgerSummary{
		TotalCharges:    totalCharges,
		TotalRefunds:    totalRefunds,
		NetRevenue:      totalCharges - totalRefunds,
		ChargeCount:     s.transactionRepo.CountByType(models.TransactionTypeCharge),
		RefundCount:     s.transactionRepo.CountByType(models.TransactionTypeRefund),
		TransactionCount: s.transactionRepo.Count(),
	}, nil
}

func (s *LedgerService) GetTransactionsByPayment(paymentID string) ([]*models.Transaction, error) {
	return s.transactionRepo.FindByPaymentID(paymentID)
}

func (s *LedgerService) GetAllTransactions() ([]*models.Transaction, error) {
	return s.transactionRepo.GetAll()
}

func (s *LedgerService) GetChargeTransactions() ([]*models.Transaction, error) {
	return s.transactionRepo.FindByType(models.TransactionTypeCharge)
}

func (s *LedgerService) GetRefundTransactions() ([]*models.Transaction, error) {
	return s.transactionRepo.FindByType(models.TransactionTypeRefund)
}

