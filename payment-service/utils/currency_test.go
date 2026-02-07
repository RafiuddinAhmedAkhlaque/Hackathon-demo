package utils

import (
	"testing"
)

func TestValidateCurrency_Valid(t *testing.T) {
	validCurrencies := []string{"USD", "EUR", "GBP", "CAD", "JPY"}
	for _, c := range validCurrencies {
		if err := ValidateCurrency(c); err != nil {
			t.Errorf("expected %s to be valid, got error: %v", c, err)
		}
	}
}

func TestValidateCurrency_CaseInsensitive(t *testing.T) {
	if err := ValidateCurrency("usd"); err != nil {
		t.Errorf("expected lowercase usd to be valid, got error: %v", err)
	}
}

func TestValidateCurrency_Invalid(t *testing.T) {
	if err := ValidateCurrency("INVALID"); err == nil {
		t.Error("expected error for invalid currency")
	}
}

func TestRoundToDecimalPlaces(t *testing.T) {
	tests := []struct {
		amount   float64
		currency string
		expected float64
	}{
		{10.456, "USD", 10.46},
		{10.454, "USD", 10.45},
		{10.5, "JPY", 11},    // JPY has 0 decimal places
		{10.4, "JPY", 10},
		{99.999, "EUR", 100.0},
	}

	for _, tt := range tests {
		result := RoundToDecimalPlaces(tt.amount, tt.currency)
		if result != tt.expected {
			t.Errorf("RoundToDecimalPlaces(%f, %s) = %f, want %f",
				tt.amount, tt.currency, result, tt.expected)
		}
	}
}

func TestFormatAmount(t *testing.T) {
	tests := []struct {
		amount   float64
		currency string
		expected string
	}{
		{10.50, "USD", "$10.50"},
		{1000, "EUR", "€1000.00"},
		{500, "JPY", "¥500"},
	}

	for _, tt := range tests {
		result := FormatAmount(tt.amount, tt.currency)
		if result != tt.expected {
			t.Errorf("FormatAmount(%f, %s) = %s, want %s",
				tt.amount, tt.currency, result, tt.expected)
		}
	}
}

func TestConvertCurrency(t *testing.T) {
	// USD to EUR
	result, err := ConvertCurrency(100, "USD", "EUR")
	if err != nil {
		t.Fatalf("expected no error, got %v", err)
	}
	if result != 85.0 {
		t.Errorf("expected 85.0, got %f", result)
	}

	// Invalid from currency
	_, err = ConvertCurrency(100, "INVALID", "USD")
	if err == nil {
		t.Error("expected error for invalid source currency")
	}

	// Invalid to currency
	_, err = ConvertCurrency(100, "USD", "INVALID")
	if err == nil {
		t.Error("expected error for invalid target currency")
	}
}

