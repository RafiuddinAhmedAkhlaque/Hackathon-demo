package repositories

import (
	"fmt"
	"sync"

	"github.com/ecommerce/payment-service/models"
)

type TransactionRepository struct {
	mu           sync.RWMutex
	transactions map[string]*models.Transaction
	paymentIdx   map[string][]string // paymentID -> transactionIDs
}

func NewTransactionRepository() *TransactionRepository {
	return &TransactionRepository{
		transactions: make(map[string]*models.Transaction),
		paymentIdx:   make(map[string][]string),
	}
}

func (r *TransactionRepository) Save(tx *models.Transaction) (*models.Transaction, error) {
	r.mu.Lock()
	defer r.mu.Unlock()

	r.transactions[tx.ID] = tx

	if _, exists := r.paymentIdx[tx.PaymentID]; !exists {
		r.paymentIdx[tx.PaymentID] = []string{}
	}
	if !contains(r.paymentIdx[tx.PaymentID], tx.ID) {
		r.paymentIdx[tx.PaymentID] = append(r.paymentIdx[tx.PaymentID], tx.ID)
	}

	return tx, nil
}

func (r *TransactionRepository) FindByID(id string) (*models.Transaction, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()

	tx, ok := r.transactions[id]
	if !ok {
		return nil, fmt.Errorf("transaction not found: %s", id)
	}
	return tx, nil
}

func (r *TransactionRepository) FindByPaymentID(paymentID string) ([]*models.Transaction, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()

	ids := r.paymentIdx[paymentID]
	result := make([]*models.Transaction, 0, len(ids))
	for _, id := range ids {
		if tx, ok := r.transactions[id]; ok {
			result = append(result, tx)
		}
	}
	return result, nil
}

func (r *TransactionRepository) FindByType(txType models.TransactionType) ([]*models.Transaction, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()

	result := make([]*models.Transaction, 0)
	for _, tx := range r.transactions {
		if tx.Type == txType {
			result = append(result, tx)
		}
	}
	return result, nil
}

func (r *TransactionRepository) GetAll() ([]*models.Transaction, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()

	result := make([]*models.Transaction, 0, len(r.transactions))
	for _, tx := range r.transactions {
		result = append(result, tx)
	}
	return result, nil
}

func (r *TransactionRepository) GetTotalByType(txType models.TransactionType) (float64, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()

	var total float64
	for _, tx := range r.transactions {
		if tx.Type == txType {
			total += tx.Amount
		}
	}
	return total, nil
}

func (r *TransactionRepository) Count() int {
	r.mu.RLock()
	defer r.mu.RUnlock()
	return len(r.transactions)
}

func (r *TransactionRepository) CountByType(txType models.TransactionType) int {
	r.mu.RLock()
	defer r.mu.RUnlock()

	count := 0
	for _, tx := range r.transactions {
		if tx.Type == txType {
			count++
		}
	}
	return count
}

