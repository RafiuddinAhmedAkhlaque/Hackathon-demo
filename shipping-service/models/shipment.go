package models

import "time"

type ShipmentStatus string

const (
	ShipmentStatusCreated    ShipmentStatus = "created"
	ShipmentStatusPickedUp   ShipmentStatus = "picked_up"
	ShipmentStatusInTransit  ShipmentStatus = "in_transit"
	ShipmentStatusOutForDelivery ShipmentStatus = "out_for_delivery"
	ShipmentStatusDelivered  ShipmentStatus = "delivered"
	ShipmentStatusReturned   ShipmentStatus = "returned"
	ShipmentStatusCancelled  ShipmentStatus = "cancelled"
)

type Shipment struct {
	ID              string         `json:"id"`
	OrderID         string         `json:"order_id"`
	CarrierCode     string         `json:"carrier_code"`
	TrackingNumber  string         `json:"tracking_number"`
	Status          ShipmentStatus `json:"status"`
	FromAddress     Address        `json:"from_address"`
	ToAddress       Address        `json:"to_address"`
	Weight          float64        `json:"weight"`          // in kg
	Dimensions      Dimensions     `json:"dimensions"`
	ShippingRate    float64        `json:"shipping_rate"`
	EstimatedDelivery time.Time    `json:"estimated_delivery"`
	ActualDelivery  *time.Time     `json:"actual_delivery,omitempty"`
	CreatedAt       time.Time      `json:"created_at"`
	UpdatedAt       time.Time      `json:"updated_at"`
}

