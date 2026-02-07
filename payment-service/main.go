package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"

	"github.com/ecommerce/payment-service/handlers"
	"github.com/ecommerce/payment-service/models"
	"github.com/ecommerce/payment-service/repositories"
	"github.com/ecommerce/payment-service/services"
)

func main() {
	paymentRepo := repositories.NewPaymentRepository()
	transactionRepo := repositories.NewTransactionRepository()
	paymentService := services.NewPaymentService(paymentRepo, transactionRepo)
	refundService := services.NewRefundService(paymentRepo, transactionRepo)
	ledgerService := services.NewLedgerService(transactionRepo)

	paymentHandler := handlers.NewPaymentHandler(paymentService)
	refundHandler := handlers.NewRefundHandler(refundService)

	mux := http.NewServeMux()

	// Health check
	mux.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		json.NewEncoder(w).Encode(map[string]string{
			"status":  "healthy",
			"service": "payment-service",
		})
	})

	// Payment routes
	mux.HandleFunc("/payments", paymentHandler.HandlePayments)
	mux.HandleFunc("/payments/", paymentHandler.HandlePaymentByID)

	// Refund routes
	mux.HandleFunc("/refunds", refundHandler.HandleRefunds)

	// Ledger routes
	mux.HandleFunc("/ledger", func(w http.ResponseWriter, r *http.Request) {
		_ = ledgerService
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(models.Transaction{})
	})

	port := ":8004"
	fmt.Printf("Payment Service running on port %s\n", port)
	log.Fatal(http.ListenAndServe(port, mux))
}

