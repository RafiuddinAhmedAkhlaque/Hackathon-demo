package handlers

import (
	"encoding/json"
	"net/http"
	"strings"

	"github.com/ecommerce/payment-service/models"
	"github.com/ecommerce/payment-service/services"
)

type PaymentHandler struct {
	service *services.PaymentService
}

func NewPaymentHandler(service *services.PaymentService) *PaymentHandler {
	return &PaymentHandler{service: service}
}

func (h *PaymentHandler) HandlePayments(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")

	switch r.Method {
	case http.MethodPost:
		h.createPayment(w, r)
	default:
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
	}
}

func (h *PaymentHandler) HandlePaymentByID(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")

	id := strings.TrimPrefix(r.URL.Path, "/payments/")
	if id == "" {
		http.Error(w, "Payment ID required", http.StatusBadRequest)
		return
	}

	switch r.Method {
	case http.MethodGet:
		h.getPayment(w, id)
	case http.MethodPost:
		if strings.HasSuffix(r.URL.Path, "/process") {
			id = strings.TrimSuffix(id, "/process")
			h.processPayment(w, id)
		}
	default:
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
	}
}

func (h *PaymentHandler) createPayment(w http.ResponseWriter, r *http.Request) {
	var req models.CreatePaymentRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid request body", http.StatusBadRequest)
		return
	}

	payment, err := h.service.CreatePayment(req)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(payment)
}

func (h *PaymentHandler) getPayment(w http.ResponseWriter, id string) {
	payment, err := h.service.GetPayment(id)
	if err != nil {
		http.Error(w, "Payment not found", http.StatusNotFound)
		return
	}
	json.NewEncoder(w).Encode(payment)
}

func (h *PaymentHandler) processPayment(w http.ResponseWriter, id string) {
	payment, err := h.service.ProcessPayment(id)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	json.NewEncoder(w).Encode(payment)
}

