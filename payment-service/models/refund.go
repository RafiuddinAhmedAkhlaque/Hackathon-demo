package models

import "time"

type RefundStatus string

const (
	RefundStatusPending   RefundStatus = "pending"
	RefundStatusCompleted RefundStatus = "completed"
	RefundStatusFailed    RefundStatus = "failed"
)

type Refund struct {
	ID        string       `json:"id"`
	PaymentID string       `json:"payment_id"`
	Amount    float64      `json:"amount"`
	Reason    string       `json:"reason"`
	Status    RefundStatus `json:"status"`
	CreatedAt time.Time    `json:"created_at"`
}

type CreateRefundRequest struct {
	PaymentID string  `json:"payment_id"`
	Amount    float64 `json:"amount"`
	Reason    string  `json:"reason"`
}

