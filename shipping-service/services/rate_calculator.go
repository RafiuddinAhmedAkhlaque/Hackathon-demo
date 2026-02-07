package services

import (
	"fmt"
	"sort"

	"github.com/ecommerce/shipping-service/carriers"
	"github.com/ecommerce/shipping-service/models"
)

type RateCalculator struct {
	carriers []carriers.Carrier
}

func NewRateCalculator() *RateCalculator {
	return &RateCalculator{
		carriers: carriers.GetAllCarriers(),
	}
}

func NewRateCalculatorWithCarriers(c []carriers.Carrier) *RateCalculator {
	return &RateCalculator{carriers: c}
}

func (rc *RateCalculator) GetAllRates(req models.RateRequest) ([]models.ShippingRate, error) {
	if err := rc.validateRequest(req); err != nil {
		return nil, err
	}

	var allRates []models.ShippingRate

	for _, carrier := range rc.carriers {
		rates, err := carrier.CalculateRates(req)
		if err != nil {
			continue // Skip carriers that can't handle this shipment
		}
		allRates = append(allRates, rates...)
	}

	return allRates, nil
}

func (rc *RateCalculator) GetRatesByCarrier(carrierCode string, req models.RateRequest) ([]models.ShippingRate, error) {
	if err := rc.validateRequest(req); err != nil {
		return nil, err
	}

	carrier := carriers.GetCarrierByCode(carrierCode)
	if carrier == nil {
		return nil, fmt.Errorf("carrier '%s' not found", carrierCode)
	}

	return carrier.CalculateRates(req)
}

func (rc *RateCalculator) GetCheapestRate(req models.RateRequest) (*models.ShippingRate, error) {
	rates, err := rc.GetAllRates(req)
	if err != nil {
		return nil, err
	}

	if len(rates) == 0 {
		return nil, fmt.Errorf("no rates available")
	}

	sort.Slice(rates, func(i, j int) bool {
		return rates[i].Rate < rates[j].Rate
	})

	return &rates[0], nil
}

func (rc *RateCalculator) GetFastestRate(req models.RateRequest) (*models.ShippingRate, error) {
	rates, err := rc.GetAllRates(req)
	if err != nil {
		return nil, err
	}

	if len(rates) == 0 {
		return nil, fmt.Errorf("no rates available")
	}

	sort.Slice(rates, func(i, j int) bool {
		return rates[i].EstimatedDays < rates[j].EstimatedDays
	})

	return &rates[0], nil
}

func (rc *RateCalculator) GetRatesBySortOrder(req models.RateRequest, sortBy string) ([]models.ShippingRate, error) {
	rates, err := rc.GetAllRates(req)
	if err != nil {
		return nil, err
	}

	switch sortBy {
	case "price":
		sort.Slice(rates, func(i, j int) bool { return rates[i].Rate < rates[j].Rate })
	case "speed":
		sort.Slice(rates, func(i, j int) bool { return rates[i].EstimatedDays < rates[j].EstimatedDays })
	case "carrier":
		sort.Slice(rates, func(i, j int) bool { return rates[i].CarrierCode < rates[j].CarrierCode })
	}

	return rates, nil
}

func (rc *RateCalculator) validateRequest(req models.RateRequest) error {
	if req.Weight <= 0 {
		return fmt.Errorf("weight must be positive")
	}
	if req.FromZip == "" {
		return fmt.Errorf("from zip code is required")
	}
	if req.ToZip == "" {
		return fmt.Errorf("to zip code is required")
	}
	return nil
}

