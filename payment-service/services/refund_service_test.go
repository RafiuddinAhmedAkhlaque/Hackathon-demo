package services

import (
	"testing"

	"github.com/ecommerce/payment-service/models"
	"github.com/ecommerce/payment-service/repositories"
)

func setupRefundTest() (*RefundService, *PaymentService, *repositories.PaymentRepository, *repositories.TransactionRepository) {
	paymentRepo := repositories.NewPaymentRepository()
	txRepo := repositories.NewTransactionRepository()
	paymentService := NewPaymentService(paymentRepo, txRepo)
	refundService := NewRefundService(paymentRepo, txRepo)
	return refundService, paymentService, paymentRepo, txRepo
}

func createCompletedPayment(paymentService *PaymentService) *models.Payment {
	payment, _ := paymentService.CreatePayment(models.CreatePaymentRequest{
		OrderID:  "order-123",
		UserID:   "user-456",
		Amount:   100.00,
		Currency: "USD",
		MethodID: "method-789",
	})
	processed, _ := paymentService.ProcessPayment(payment.ID)
	return processed
}

func TestCreateRefund_Success(t *testing.T) {
	refundService, paymentService, _, _ := setupRefundTest()
	payment := createCompletedPayment(paymentService)

	refund, err := refundService.CreateRefund(models.CreateRefundRequest{
		PaymentID: payment.ID,
		Amount:    50.00,
		Reason:    "Customer request",
	})

	if err != nil {
		t.Fatalf("expected no error, got %v", err)
	}
	if refund.Amount != 50.00 {
		t.Errorf("expected refund amount 50.00, got %.2f", refund.Amount)
	}
	if refund.Status != models.RefundStatusCompleted {
		t.Errorf("expected refund status completed, got %s", refund.Status)
	}
}

func TestCreateRefund_FullRefund(t *testing.T) {
	refundService, paymentService, paymentRepo, _ := setupRefundTest()
	payment := createCompletedPayment(paymentService)

	_, err := refundService.CreateRefund(models.CreateRefundRequest{
		PaymentID: payment.ID,
		Amount:    100.00,
		Reason:    "Full refund",
	})

	if err != nil {
		t.Fatalf("expected no error, got %v", err)
	}

	// Verify payment status changed to refunded
	updated, _ := paymentRepo.FindByID(payment.ID)
	if updated.Status != models.PaymentStatusRefunded {
		t.Errorf("expected payment status refunded, got %s", updated.Status)
	}
}

func TestCreateRefund_ExceedsPaymentAmount(t *testing.T) {
	refundService, paymentService, _, _ := setupRefundTest()
	payment := createCompletedPayment(paymentService)

	_, err := refundService.CreateRefund(models.CreateRefundRequest{
		PaymentID: payment.ID,
		Amount:    150.00,
		Reason:    "Too much",
	})

	if err == nil {
		t.Error("expected error for refund exceeding payment amount")
	}
}

func TestCreateRefund_PartialRefunds(t *testing.T) {
	refundService, paymentService, _, _ := setupRefundTest()
	payment := createCompletedPayment(paymentService)

	// First partial refund
	_, err := refundService.CreateRefund(models.CreateRefundRequest{
		PaymentID: payment.ID,
		Amount:    40.00,
		Reason:    "Partial refund 1",
	})
	if err != nil {
		t.Fatalf("expected no error, got %v", err)
	}

	// Second partial refund
	_, err = refundService.CreateRefund(models.CreateRefundRequest{
		PaymentID: payment.ID,
		Amount:    40.00,
		Reason:    "Partial refund 2",
	})
	if err != nil {
		t.Fatalf("expected no error, got %v", err)
	}

	// Third refund should fail (would exceed total)
	_, err = refundService.CreateRefund(models.CreateRefundRequest{
		PaymentID: payment.ID,
		Amount:    30.00,
		Reason:    "Too much total",
	})
	if err == nil {
		t.Error("expected error for exceeding total payment amount")
	}
}

func TestCreateRefund_PaymentNotFound(t *testing.T) {
	refundService, _, _, _ := setupRefundTest()

	_, err := refundService.CreateRefund(models.CreateRefundRequest{
		PaymentID: "nonexistent",
		Amount:    50.00,
		Reason:    "Test",
	})

	if err == nil {
		t.Error("expected error for nonexistent payment")
	}
}

func TestCreateRefund_PaymentNotCompleted(t *testing.T) {
	refundService, paymentService, _, _ := setupRefundTest()
	payment, _ := paymentService.CreatePayment(models.CreatePaymentRequest{
		OrderID:  "order-123",
		UserID:   "user-456",
		Amount:   100.00,
		Currency: "USD",
		MethodID: "method-789",
	})
	// Don't process the payment

	_, err := refundService.CreateRefund(models.CreateRefundRequest{
		PaymentID: payment.ID,
		Amount:    50.00,
		Reason:    "Test",
	})

	if err == nil {
		t.Error("expected error for refunding unprocessed payment")
	}
}

func TestCreateRefund_MissingReason(t *testing.T) {
	refundService, paymentService, _, _ := setupRefundTest()
	payment := createCompletedPayment(paymentService)

	_, err := refundService.CreateRefund(models.CreateRefundRequest{
		PaymentID: payment.ID,
		Amount:    50.00,
		Reason:    "",
	})

	if err == nil {
		t.Error("expected error for missing reason")
	}
}

func TestGetRefundsForPayment(t *testing.T) {
	refundService, paymentService, _, _ := setupRefundTest()
	payment := createCompletedPayment(paymentService)

	refundService.CreateRefund(models.CreateRefundRequest{
		PaymentID: payment.ID,
		Amount:    30.00,
		Reason:    "Refund 1",
	})
	refundService.CreateRefund(models.CreateRefundRequest{
		PaymentID: payment.ID,
		Amount:    20.00,
		Reason:    "Refund 2",
	})

	refunds, err := refundService.GetRefundsForPayment(payment.ID)
	if err != nil {
		t.Fatalf("expected no error, got %v", err)
	}
	if len(refunds) != 2 {
		t.Errorf("expected 2 refunds, got %d", len(refunds))
	}
}

