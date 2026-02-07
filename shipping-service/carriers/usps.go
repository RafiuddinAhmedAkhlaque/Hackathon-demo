package carriers

import (
	"fmt"
	"github.com/ecommerce/shipping-service/models"
)

type USPSCarrier struct {
	BaseCarrier
}

func NewUSPSCarrier() *USPSCarrier {
	return &USPSCarrier{
		BaseCarrier: BaseCarrier{Code: "usps", Name: "USPS"},
	}
}

func (u *USPSCarrier) CalculateRates(req models.RateRequest) ([]models.ShippingRate, error) {
	if req.Weight <= 0 {
		return nil, fmt.Errorf("weight must be positive")
	}
	if req.Weight > 31.75 { // USPS max weight ~70 lbs
		return nil, fmt.Errorf("USPS weight limit exceeded (max 31.75 kg)")
	}

	baseRate := req.Weight * 1.80

	return []models.ShippingRate{
		{
			CarrierCode:   u.Code,
			CarrierName:   u.Name,
			ServiceType:   "first_class",
			Rate:          round(baseRate*0.7, 2),
			Currency:      "USD",
			EstimatedDays: 5,
			IsGuaranteed:  false,
		},
		{
			CarrierCode:   u.Code,
			CarrierName:   u.Name,
			ServiceType:   "priority",
			Rate:          round(baseRate, 2),
			Currency:      "USD",
			EstimatedDays: 3,
			IsGuaranteed:  false,
		},
		{
			CarrierCode:   u.Code,
			CarrierName:   u.Name,
			ServiceType:   "priority_express",
			Rate:          round(baseRate*2.5, 2),
			Currency:      "USD",
			EstimatedDays: 1,
			IsGuaranteed:  true,
		},
	}, nil
}

func (u *USPSCarrier) GetEstimatedDays(serviceType string, fromZip, toZip string) int {
	switch serviceType {
	case "first_class":
		return 5
	case "priority":
		return 3
	case "priority_express":
		return 1
	default:
		return 7
	}
}

func (u *USPSCarrier) ValidateAddress(addr models.Address) error {
	if addr.PostalCode == "" {
		return fmt.Errorf("postal code is required for USPS")
	}
	return nil
}

