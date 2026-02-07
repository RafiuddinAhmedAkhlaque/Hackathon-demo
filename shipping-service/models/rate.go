package models

type ShippingRate struct {
	CarrierCode    string  `json:"carrier_code"`
	CarrierName    string  `json:"carrier_name"`
	ServiceType    string  `json:"service_type"`
	Rate           float64 `json:"rate"`
	Currency       string  `json:"currency"`
	EstimatedDays  int     `json:"estimated_days"`
	IsGuaranteed   bool    `json:"is_guaranteed"`
}

type RateRequest struct {
	FromZip    string     `json:"from_zip"`
	ToZip      string     `json:"to_zip"`
	Weight     float64    `json:"weight"`
	Dimensions Dimensions `json:"dimensions"`
}

type Dimensions struct {
	Length float64 `json:"length"`
	Width  float64 `json:"width"`
	Height float64 `json:"height"`
	Unit   string  `json:"unit"` // "cm" or "in"
}

