package utils

import (
	"fmt"
	"math"
	"strings"
)

// SupportedCurrencies lists all valid currency codes
var SupportedCurrencies = map[string]CurrencyInfo{
	"USD": {Code: "USD", Symbol: "$", DecimalPlaces: 2},
	"EUR": {Code: "EUR", Symbol: "€", DecimalPlaces: 2},
	"GBP": {Code: "GBP", Symbol: "£", DecimalPlaces: 2},
	"CAD": {Code: "CAD", Symbol: "CA$", DecimalPlaces: 2},
	"JPY": {Code: "JPY", Symbol: "¥", DecimalPlaces: 0},
}

type CurrencyInfo struct {
	Code          string
	Symbol        string
	DecimalPlaces int
}

// ValidateCurrency checks if a currency code is supported
func ValidateCurrency(code string) error {
	upper := strings.ToUpper(code)
	if _, ok := SupportedCurrencies[upper]; !ok {
		return fmt.Errorf("unsupported currency: %s", code)
	}
	return nil
}

// RoundToDecimalPlaces rounds a monetary amount appropriately for the currency
func RoundToDecimalPlaces(amount float64, currency string) float64 {
	info, ok := SupportedCurrencies[strings.ToUpper(currency)]
	if !ok {
		// Default to 2 decimal places
		info = CurrencyInfo{DecimalPlaces: 2}
	}
	factor := math.Pow(10, float64(info.DecimalPlaces))
	return math.Round(amount*factor) / factor
}

// FormatAmount formats a monetary amount with the currency symbol
func FormatAmount(amount float64, currency string) string {
	info, ok := SupportedCurrencies[strings.ToUpper(currency)]
	if !ok {
		return fmt.Sprintf("%.2f %s", amount, currency)
	}
	format := fmt.Sprintf("%s%%.%df", info.Symbol, info.DecimalPlaces)
	return fmt.Sprintf(format, amount)
}

// ConvertCurrency provides simple conversion between currencies (mock rates)
func ConvertCurrency(amount float64, from, to string) (float64, error) {
	if err := ValidateCurrency(from); err != nil {
		return 0, err
	}
	if err := ValidateCurrency(to); err != nil {
		return 0, err
	}

	// Mock exchange rates (relative to USD)
	rates := map[string]float64{
		"USD": 1.0,
		"EUR": 0.85,
		"GBP": 0.73,
		"CAD": 1.36,
		"JPY": 149.50,
	}

	fromRate := rates[strings.ToUpper(from)]
	toRate := rates[strings.ToUpper(to)]

	usdAmount := amount / fromRate
	converted := usdAmount * toRate

	return RoundToDecimalPlaces(converted, to), nil
}

