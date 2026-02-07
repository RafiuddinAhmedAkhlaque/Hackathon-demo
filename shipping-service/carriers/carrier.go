package carriers

import "github.com/ecommerce/shipping-service/models"

// Carrier defines the interface that all shipping carriers must implement.
type Carrier interface {
	GetCode() string
	GetName() string
	CalculateRates(req models.RateRequest) ([]models.ShippingRate, error)
	GetEstimatedDays(serviceType string, fromZip, toZip string) int
	ValidateAddress(addr models.Address) error
}

// BaseCarrier provides common functionality for all carriers.
type BaseCarrier struct {
	Code string
	Name string
}

func (b *BaseCarrier) GetCode() string { return b.Code }
func (b *BaseCarrier) GetName() string { return b.Name }

// GetAllCarriers returns all supported carriers.
func GetAllCarriers() []Carrier {
	return []Carrier{
		NewFedExCarrier(),
		NewUPSCarrier(),
		NewUSPSCarrier(),
	}
}

// GetCarrierByCode returns a carrier by its code.
func GetCarrierByCode(code string) Carrier {
	for _, c := range GetAllCarriers() {
		if c.GetCode() == code {
			return c
		}
	}
	return nil
}

