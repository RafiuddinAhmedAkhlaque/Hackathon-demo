package models

import "time"

type PaymentStatus string

const (
	PaymentStatusPending   PaymentStatus = "pending"
	PaymentStatusCompleted PaymentStatus = "completed"
	PaymentStatusFailed    PaymentStatus = "failed"
	PaymentStatusRefunded  PaymentStatus = "refunded"
	PaymentStatusCancelled PaymentStatus = "cancelled"
)

type Payment struct {
	ID            string        `json:"id"`
	OrderID       string        `json:"order_id"`
	UserID        string        `json:"user_id"`
	Amount        float64       `json:"amount"`
	Currency      string        `json:"currency"`
	Status        PaymentStatus `json:"status"`
	MethodID      string        `json:"method_id"`
	Description   string        `json:"description"`
	TransactionID string        `json:"transaction_id,omitempty"`
	CreatedAt     time.Time     `json:"created_at"`
	UpdatedAt     time.Time     `json:"updated_at"`
}

type CreatePaymentRequest struct {
	OrderID     string  `json:"order_id"`
	UserID      string  `json:"user_id"`
	Amount      float64 `json:"amount"`
	Currency    string  `json:"currency"`
	MethodID    string  `json:"method_id"`
	Description string  `json:"description"`
}

