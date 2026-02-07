package utils

import (
	"fmt"
	"strings"
)

// ValidateRequired checks if a string field is non-empty
func ValidateRequired(value, fieldName string) error {
	if strings.TrimSpace(value) == "" {
		return fmt.Errorf("%s is required", fieldName)
	}
	return nil
}

// ValidatePositiveAmount checks if an amount is positive
func ValidatePositiveAmount(amount float64, fieldName string) error {
	if amount <= 0 {
		return fmt.Errorf("%s must be a positive amount", fieldName)
	}
	return nil
}

// ValidateNonNegativeAmount checks if an amount is non-negative
func ValidateNonNegativeAmount(amount float64, fieldName string) error {
	if amount < 0 {
		return fmt.Errorf("%s cannot be negative", fieldName)
	}
	return nil
}

// ValidateMaxAmount checks if an amount doesn't exceed a maximum
func ValidateMaxAmount(amount, max float64, fieldName string) error {
	if amount > max {
		return fmt.Errorf("%s cannot exceed %.2f", fieldName, max)
	}
	return nil
}

// ValidationErrors collects multiple validation errors
type ValidationErrors struct {
	Errors []string
}

func NewValidationErrors() *ValidationErrors {
	return &ValidationErrors{Errors: make([]string, 0)}
}

func (ve *ValidationErrors) Add(err error) {
	if err != nil {
		ve.Errors = append(ve.Errors, err.Error())
	}
}

func (ve *ValidationErrors) HasErrors() bool {
	return len(ve.Errors) > 0
}

func (ve *ValidationErrors) Error() string {
	return strings.Join(ve.Errors, "; ")
}

