package models

import "time"

type PaymentMethodType string

const (
	MethodTypeCreditCard  PaymentMethodType = "credit_card"
	MethodTypeDebitCard   PaymentMethodType = "debit_card"
	MethodTypeBankAccount PaymentMethodType = "bank_account"
	MethodTypeDigitalWallet PaymentMethodType = "digital_wallet"
)

type PaymentMethod struct {
	ID        string            `json:"id"`
	UserID    string            `json:"user_id"`
	Type      PaymentMethodType `json:"type"`
	Last4     string            `json:"last4"`
	Brand     string            `json:"brand,omitempty"`
	IsDefault bool              `json:"is_default"`
	IsActive  bool              `json:"is_active"`
	CreatedAt time.Time         `json:"created_at"`
}

