package models

import "time"

type TrackingEvent struct {
	ID          string    `json:"id"`
	ShipmentID  string    `json:"shipment_id"`
	Status      string    `json:"status"`
	Location    string    `json:"location"`
	Description string    `json:"description"`
	Timestamp   time.Time `json:"timestamp"`
}

