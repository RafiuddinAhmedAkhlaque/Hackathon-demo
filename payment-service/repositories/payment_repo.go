package repositories

import (
	"fmt"
	"sync"

	"github.com/ecommerce/payment-service/models"
)

type PaymentRepository struct {
	mu       sync.RWMutex
	payments map[string]*models.Payment
	orderIdx map[string][]string // orderID -> paymentIDs
	userIdx  map[string][]string // userID -> paymentIDs
}

func NewPaymentRepository() *PaymentRepository {
	return &PaymentRepository{
		payments: make(map[string]*models.Payment),
		orderIdx: make(map[string][]string),
		userIdx:  make(map[string][]string),
	}
}

func (r *PaymentRepository) Save(payment *models.Payment) (*models.Payment, error) {
	r.mu.Lock()
	defer r.mu.Unlock()

	r.payments[payment.ID] = payment

	// Update indexes
	if _, exists := r.orderIdx[payment.OrderID]; !exists {
		r.orderIdx[payment.OrderID] = []string{}
	}
	if !contains(r.orderIdx[payment.OrderID], payment.ID) {
		r.orderIdx[payment.OrderID] = append(r.orderIdx[payment.OrderID], payment.ID)
	}

	if _, exists := r.userIdx[payment.UserID]; !exists {
		r.userIdx[payment.UserID] = []string{}
	}
	if !contains(r.userIdx[payment.UserID], payment.ID) {
		r.userIdx[payment.UserID] = append(r.userIdx[payment.UserID], payment.ID)
	}

	return payment, nil
}

func (r *PaymentRepository) FindByID(id string) (*models.Payment, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()

	payment, ok := r.payments[id]
	if !ok {
		return nil, fmt.Errorf("payment not found: %s", id)
	}
	return payment, nil
}

func (r *PaymentRepository) FindByOrderID(orderID string) ([]*models.Payment, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()

	ids := r.orderIdx[orderID]
	result := make([]*models.Payment, 0, len(ids))
	for _, id := range ids {
		if p, ok := r.payments[id]; ok {
			result = append(result, p)
		}
	}
	return result, nil
}

func (r *PaymentRepository) FindByUserID(userID string) ([]*models.Payment, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()

	ids := r.userIdx[userID]
	result := make([]*models.Payment, 0, len(ids))
	for _, id := range ids {
		if p, ok := r.payments[id]; ok {
			result = append(result, p)
		}
	}
	return result, nil
}

func (r *PaymentRepository) FindByStatus(status models.PaymentStatus) ([]*models.Payment, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()

	result := make([]*models.Payment, 0)
	for _, p := range r.payments {
		if p.Status == status {
			result = append(result, p)
		}
	}
	return result, nil
}

func (r *PaymentRepository) Delete(id string) error {
	r.mu.Lock()
	defer r.mu.Unlock()

	_, ok := r.payments[id]
	if !ok {
		return fmt.Errorf("payment not found: %s", id)
	}
	delete(r.payments, id)
	return nil
}

func (r *PaymentRepository) Count() int {
	r.mu.RLock()
	defer r.mu.RUnlock()
	return len(r.payments)
}

func contains(slice []string, item string) bool {
	for _, s := range slice {
		if s == item {
			return true
		}
	}
	return false
}

