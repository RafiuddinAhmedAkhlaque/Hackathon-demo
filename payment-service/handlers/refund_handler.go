package handlers

import (
	"encoding/json"
	"net/http"

	"github.com/ecommerce/payment-service/models"
	"github.com/ecommerce/payment-service/services"
)

type RefundHandler struct {
	service *services.RefundService
}

func NewRefundHandler(service *services.RefundService) *RefundHandler {
	return &RefundHandler{service: service}
}

func (h *RefundHandler) HandleRefunds(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")

	switch r.Method {
	case http.MethodPost:
		h.createRefund(w, r)
	default:
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
	}
}

func (h *RefundHandler) createRefund(w http.ResponseWriter, r *http.Request) {
	var req models.CreateRefundRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid request body", http.StatusBadRequest)
		return
	}

	refund, err := h.service.CreateRefund(req)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(refund)
}

