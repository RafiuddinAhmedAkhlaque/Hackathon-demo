package services

import (
	"testing"

	"github.com/ecommerce/payment-service/models"
	"github.com/ecommerce/payment-service/repositories"
)

func setupPaymentTest() (*PaymentService, *repositories.PaymentRepository, *repositories.TransactionRepository) {
	paymentRepo := repositories.NewPaymentRepository()
	txRepo := repositories.NewTransactionRepository()
	service := NewPaymentService(paymentRepo, txRepo)
	return service, paymentRepo, txRepo
}

func validPaymentRequest() models.CreatePaymentRequest {
	return models.CreatePaymentRequest{
		OrderID:     "order-123",
		UserID:      "user-456",
		Amount:      99.99,
		Currency:    "USD",
		MethodID:    "method-789",
		Description: "Test payment",
	}
}

func TestCreatePayment_Success(t *testing.T) {
	service, _, _ := setupPaymentTest()
	payment, err := service.CreatePayment(validPaymentRequest())

	if err != nil {
		t.Fatalf("expected no error, got %v", err)
	}
	if payment.ID == "" {
		t.Error("expected payment ID to be set")
	}
	if payment.Status != models.PaymentStatusPending {
		t.Errorf("expected status pending, got %s", payment.Status)
	}
	if payment.Amount != 99.99 {
		t.Errorf("expected amount 99.99, got %.2f", payment.Amount)
	}
}

func TestCreatePayment_MissingOrderID(t *testing.T) {
	service, _, _ := setupPaymentTest()
	req := validPaymentRequest()
	req.OrderID = ""

	_, err := service.CreatePayment(req)
	if err == nil {
		t.Error("expected error for missing order ID")
	}
}

func TestCreatePayment_InvalidAmount(t *testing.T) {
	service, _, _ := setupPaymentTest()
	req := validPaymentRequest()
	req.Amount = -10

	_, err := service.CreatePayment(req)
	if err == nil {
		t.Error("expected error for negative amount")
	}
}

func TestCreatePayment_InvalidCurrency(t *testing.T) {
	service, _, _ := setupPaymentTest()
	req := validPaymentRequest()
	req.Currency = "INVALID"

	_, err := service.CreatePayment(req)
	if err == nil {
		t.Error("expected error for invalid currency")
	}
}

func TestProcessPayment_Success(t *testing.T) {
	service, _, txRepo := setupPaymentTest()
	payment, _ := service.CreatePayment(validPaymentRequest())
	processed, err := service.ProcessPayment(payment.ID)

	if err != nil {
		t.Fatalf("expected no error, got %v", err)
	}
	if processed.Status != models.PaymentStatusCompleted {
		t.Errorf("expected status completed, got %s", processed.Status)
	}
	if processed.TransactionID == "" {
		t.Error("expected transaction ID to be set")
	}

	// Verify transaction was created
	if txRepo.Count() != 1 {
		t.Errorf("expected 1 transaction, got %d", txRepo.Count())
	}
}

func TestProcessPayment_AlreadyProcessed(t *testing.T) {
	service, _, _ := setupPaymentTest()
	payment, _ := service.CreatePayment(validPaymentRequest())
	service.ProcessPayment(payment.ID)

	_, err := service.ProcessPayment(payment.ID)
	if err == nil {
		t.Error("expected error for already processed payment")
	}
}

func TestProcessPayment_NotFound(t *testing.T) {
	service, _, _ := setupPaymentTest()
	_, err := service.ProcessPayment("nonexistent")
	if err == nil {
		t.Error("expected error for nonexistent payment")
	}
}

func TestCancelPayment_Success(t *testing.T) {
	service, _, _ := setupPaymentTest()
	payment, _ := service.CreatePayment(validPaymentRequest())
	cancelled, err := service.CancelPayment(payment.ID)

	if err != nil {
		t.Fatalf("expected no error, got %v", err)
	}
	if cancelled.Status != models.PaymentStatusCancelled {
		t.Errorf("expected status cancelled, got %s", cancelled.Status)
	}
}

func TestCancelPayment_NotPending(t *testing.T) {
	service, _, _ := setupPaymentTest()
	payment, _ := service.CreatePayment(validPaymentRequest())
	service.ProcessPayment(payment.ID)

	_, err := service.CancelPayment(payment.ID)
	if err == nil {
		t.Error("expected error for cancelling completed payment")
	}
}

func TestGetPaymentsByUser(t *testing.T) {
	service, _, _ := setupPaymentTest()
	service.CreatePayment(validPaymentRequest())

	req2 := validPaymentRequest()
	req2.OrderID = "order-456"
	service.CreatePayment(req2)

	payments, err := service.GetPaymentsByUser("user-456")
	if err != nil {
		t.Fatalf("expected no error, got %v", err)
	}
	if len(payments) != 2 {
		t.Errorf("expected 2 payments, got %d", len(payments))
	}
}

func TestGetPaymentTotal(t *testing.T) {
	service, _, _ := setupPaymentTest()

	req1 := validPaymentRequest()
	req1.Amount = 50.00
	p1, _ := service.CreatePayment(req1)
	service.ProcessPayment(p1.ID)

	req2 := validPaymentRequest()
	req2.OrderID = "order-456"
	req2.Amount = 30.00
	p2, _ := service.CreatePayment(req2)
	service.ProcessPayment(p2.ID)

	total, err := service.GetPaymentTotal("user-456")
	if err != nil {
		t.Fatalf("expected no error, got %v", err)
	}
	if total != 80.00 {
		t.Errorf("expected total 80.00, got %.2f", total)
	}
}

