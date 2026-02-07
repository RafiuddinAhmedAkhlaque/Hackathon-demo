package carriers

import (
	"fmt"
	"github.com/ecommerce/shipping-service/models"
)

type FedExCarrier struct {
	BaseCarrier
}

func NewFedExCarrier() *FedExCarrier {
	return &FedExCarrier{
		BaseCarrier: BaseCarrier{Code: "fedex", Name: "FedEx"},
	}
}

func (f *FedExCarrier) CalculateRates(req models.RateRequest) ([]models.ShippingRate, error) {
	if req.Weight <= 0 {
		return nil, fmt.Errorf("weight must be positive")
	}

	baseRate := req.Weight * 2.50
	volumetric := (req.Dimensions.Length * req.Dimensions.Width * req.Dimensions.Height) / 5000
	if volumetric > req.Weight {
		baseRate = volumetric * 2.50
	}

	return []models.ShippingRate{
		{
			CarrierCode:   f.Code,
			CarrierName:   f.Name,
			ServiceType:   "ground",
			Rate:          round(baseRate, 2),
			Currency:      "USD",
			EstimatedDays: 5,
			IsGuaranteed:  false,
		},
		{
			CarrierCode:   f.Code,
			CarrierName:   f.Name,
			ServiceType:   "express",
			Rate:          round(baseRate*2.5, 2),
			Currency:      "USD",
			EstimatedDays: 2,
			IsGuaranteed:  true,
		},
		{
			CarrierCode:   f.Code,
			CarrierName:   f.Name,
			ServiceType:   "overnight",
			Rate:          round(baseRate*4.0, 2),
			Currency:      "USD",
			EstimatedDays: 1,
			IsGuaranteed:  true,
		},
	}, nil
}

func (f *FedExCarrier) GetEstimatedDays(serviceType string, fromZip, toZip string) int {
	switch serviceType {
	case "ground":
		return 5
	case "express":
		return 2
	case "overnight":
		return 1
	default:
		return 7
	}
}

func (f *FedExCarrier) ValidateAddress(addr models.Address) error {
	if addr.PostalCode == "" {
		return fmt.Errorf("postal code is required for FedEx")
	}
	if addr.Country == "" {
		return fmt.Errorf("country is required for FedEx")
	}
	return nil
}

func round(val float64, precision int) float64 {
	p := 1.0
	for i := 0; i < precision; i++ {
		p *= 10
	}
	return float64(int(val*p+0.5)) / p
}

