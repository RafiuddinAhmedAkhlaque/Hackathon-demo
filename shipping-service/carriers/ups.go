package carriers

import (
	"fmt"
	"github.com/ecommerce/shipping-service/models"
)

type UPSCarrier struct {
	BaseCarrier
}

func NewUPSCarrier() *UPSCarrier {
	return &UPSCarrier{
		BaseCarrier: BaseCarrier{Code: "ups", Name: "UPS"},
	}
}

func (u *UPSCarrier) CalculateRates(req models.RateRequest) ([]models.ShippingRate, error) {
	if req.Weight <= 0 {
		return nil, fmt.Errorf("weight must be positive")
	}

	baseRate := req.Weight * 2.75

	return []models.ShippingRate{
		{
			CarrierCode:   u.Code,
			CarrierName:   u.Name,
			ServiceType:   "ground",
			Rate:          round(baseRate, 2),
			Currency:      "USD",
			EstimatedDays: 5,
			IsGuaranteed:  false,
		},
		{
			CarrierCode:   u.Code,
			CarrierName:   u.Name,
			ServiceType:   "2day",
			Rate:          round(baseRate*2.2, 2),
			Currency:      "USD",
			EstimatedDays: 2,
			IsGuaranteed:  true,
		},
		{
			CarrierCode:   u.Code,
			CarrierName:   u.Name,
			ServiceType:   "next_day_air",
			Rate:          round(baseRate*3.8, 2),
			Currency:      "USD",
			EstimatedDays: 1,
			IsGuaranteed:  true,
		},
	}, nil
}

func (u *UPSCarrier) GetEstimatedDays(serviceType string, fromZip, toZip string) int {
	switch serviceType {
	case "ground":
		return 5
	case "2day":
		return 2
	case "next_day_air":
		return 1
	default:
		return 7
	}
}

func (u *UPSCarrier) ValidateAddress(addr models.Address) error {
	if addr.Street == "" {
		return fmt.Errorf("street address is required for UPS")
	}
	if addr.PostalCode == "" {
		return fmt.Errorf("postal code is required for UPS")
	}
	return nil
}

