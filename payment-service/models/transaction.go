package models

import "time"

type TransactionType string

const (
	TransactionTypeCharge TransactionType = "charge"
	TransactionTypeRefund TransactionType = "refund"
)

type Transaction struct {
	ID        string          `json:"id"`
	PaymentID string          `json:"payment_id"`
	Type      TransactionType `json:"type"`
	Amount    float64         `json:"amount"`
	Currency  string          `json:"currency"`
	Status    string          `json:"status"`
	Metadata  map[string]string `json:"metadata,omitempty"`
	CreatedAt time.Time       `json:"created_at"`
}

