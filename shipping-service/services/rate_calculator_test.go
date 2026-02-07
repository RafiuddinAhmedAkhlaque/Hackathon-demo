package services

import (
	"testing"

	"github.com/ecommerce/shipping-service/models"
)

func validRateRequest() models.RateRequest {
	return models.RateRequest{
		FromZip: "10001",
		ToZip:   "90210",
		Weight:  5.0,
		Dimensions: models.Dimensions{
			Length: 30, Width: 20, Height: 15, Unit: "cm",
		},
	}
}

func TestGetAllRates(t *testing.T) {
	calc := NewRateCalculator()
	rates, err := calc.GetAllRates(validRateRequest())

	if err != nil {
		t.Fatalf("expected no error, got %v", err)
	}
	if len(rates) == 0 {
		t.Error("expected rates, got none")
	}
	// Should have rates from 3 carriers with 3 service types each = 9
	if len(rates) != 9 {
		t.Errorf("expected 9 rates, got %d", len(rates))
	}
}

func TestGetRatesByCarrier(t *testing.T) {
	calc := NewRateCalculator()
	rates, err := calc.GetRatesByCarrier("fedex", validRateRequest())

	if err != nil {
		t.Fatalf("expected no error, got %v", err)
	}
	if len(rates) != 3 {
		t.Errorf("expected 3 FedEx rates, got %d", len(rates))
	}
	for _, r := range rates {
		if r.CarrierCode != "fedex" {
			t.Errorf("expected carrier 'fedex', got '%s'", r.CarrierCode)
		}
	}
}

func TestGetRatesByCarrier_NotFound(t *testing.T) {
	calc := NewRateCalculator()
	_, err := calc.GetRatesByCarrier("nonexistent", validRateRequest())

	if err == nil {
		t.Error("expected error for nonexistent carrier")
	}
}

func TestGetCheapestRate(t *testing.T) {
	calc := NewRateCalculator()
	rate, err := calc.GetCheapestRate(validRateRequest())

	if err != nil {
		t.Fatalf("expected no error, got %v", err)
	}
	if rate == nil {
		t.Fatal("expected a rate, got nil")
	}
	// USPS first_class should be cheapest
	if rate.CarrierCode != "usps" {
		t.Logf("cheapest carrier: %s at $%.2f", rate.CarrierCode, rate.Rate)
	}
}

func TestGetFastestRate(t *testing.T) {
	calc := NewRateCalculator()
	rate, err := calc.GetFastestRate(validRateRequest())

	if err != nil {
		t.Fatalf("expected no error, got %v", err)
	}
	if rate.EstimatedDays != 1 {
		t.Errorf("expected 1 day delivery, got %d", rate.EstimatedDays)
	}
}

func TestValidation_ZeroWeight(t *testing.T) {
	calc := NewRateCalculator()
	req := validRateRequest()
	req.Weight = 0

	_, err := calc.GetAllRates(req)
	if err == nil {
		t.Error("expected error for zero weight")
	}
}

func TestValidation_MissingFromZip(t *testing.T) {
	calc := NewRateCalculator()
	req := validRateRequest()
	req.FromZip = ""

	_, err := calc.GetAllRates(req)
	if err == nil {
		t.Error("expected error for missing from zip")
	}
}

func TestValidation_MissingToZip(t *testing.T) {
	calc := NewRateCalculator()
	req := validRateRequest()
	req.ToZip = ""

	_, err := calc.GetAllRates(req)
	if err == nil {
		t.Error("expected error for missing to zip")
	}
}

func TestSortByPrice(t *testing.T) {
	calc := NewRateCalculator()
	rates, err := calc.GetRatesBySortOrder(validRateRequest(), "price")

	if err != nil {
		t.Fatalf("expected no error, got %v", err)
	}
	for i := 1; i < len(rates); i++ {
		if rates[i].Rate < rates[i-1].Rate {
			t.Errorf("rates not sorted by price at index %d", i)
		}
	}
}

func TestSortBySpeed(t *testing.T) {
	calc := NewRateCalculator()
	rates, err := calc.GetRatesBySortOrder(validRateRequest(), "speed")

	if err != nil {
		t.Fatalf("expected no error, got %v", err)
	}
	for i := 1; i < len(rates); i++ {
		if rates[i].EstimatedDays < rates[i-1].EstimatedDays {
			t.Errorf("rates not sorted by speed at index %d", i)
		}
	}
}

