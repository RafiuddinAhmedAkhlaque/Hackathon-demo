package services

import (
	"fmt"
	"time"

	"github.com/ecommerce/shipping-service/carriers"
	"github.com/ecommerce/shipping-service/models"
	"github.com/google/uuid"
)

type ShipmentService struct {
	shipments map[string]*models.Shipment
	events    map[string][]*models.TrackingEvent // shipmentID -> events
}

func NewShipmentService() *ShipmentService {
	return &ShipmentService{
		shipments: make(map[string]*models.Shipment),
		events:    make(map[string][]*models.TrackingEvent),
	}
}

type CreateShipmentRequest struct {
	OrderID     string
	CarrierCode string
	ServiceType string
	FromAddress models.Address
	ToAddress   models.Address
	Weight      float64
	Dimensions  models.Dimensions
}

func (s *ShipmentService) CreateShipment(req CreateShipmentRequest) (*models.Shipment, error) {
	if req.OrderID == "" {
		return nil, fmt.Errorf("order ID is required")
	}

	carrier := carriers.GetCarrierByCode(req.CarrierCode)
	if carrier == nil {
		return nil, fmt.Errorf("carrier '%s' not found", req.CarrierCode)
	}

	if err := carrier.ValidateAddress(req.ToAddress); err != nil {
		return nil, fmt.Errorf("invalid destination address: %w", err)
	}

	estimatedDays := carrier.GetEstimatedDays(req.ServiceType, req.FromAddress.PostalCode, req.ToAddress.PostalCode)

	rateReq := models.RateRequest{
		FromZip: req.FromAddress.PostalCode, ToZip: req.ToAddress.PostalCode,
		Weight: req.Weight, Dimensions: req.Dimensions,
	}
	rates, err := carrier.CalculateRates(rateReq)
	if err != nil {
		return nil, err
	}

	var rate float64
	for _, r := range rates {
		if r.ServiceType == req.ServiceType {
			rate = r.Rate
			break
		}
	}

	shipment := &models.Shipment{
		ID:                uuid.New().String(),
		OrderID:           req.OrderID,
		CarrierCode:       req.CarrierCode,
		TrackingNumber:    generateTrackingNumber(req.CarrierCode),
		Status:            models.ShipmentStatusCreated,
		FromAddress:       req.FromAddress,
		ToAddress:         req.ToAddress,
		Weight:            req.Weight,
		Dimensions:        req.Dimensions,
		ShippingRate:      rate,
		EstimatedDelivery: time.Now().AddDate(0, 0, estimatedDays),
		CreatedAt:         time.Now(),
		UpdatedAt:         time.Now(),
	}

	s.shipments[shipment.ID] = shipment
	s.addEvent(shipment.ID, "created", "Origin", "Shipment created")

	return shipment, nil
}

func (s *ShipmentService) GetShipment(id string) (*models.Shipment, error) {
	shipment, ok := s.shipments[id]
	if !ok {
		return nil, fmt.Errorf("shipment not found: %s", id)
	}
	return shipment, nil
}

func (s *ShipmentService) UpdateStatus(id string, status models.ShipmentStatus, location, description string) (*models.Shipment, error) {
	shipment, ok := s.shipments[id]
	if !ok {
		return nil, fmt.Errorf("shipment not found: %s", id)
	}

	shipment.Status = status
	shipment.UpdatedAt = time.Now()

	if status == models.ShipmentStatusDelivered {
		now := time.Now()
		shipment.ActualDelivery = &now
	}

	s.addEvent(id, string(status), location, description)

	return shipment, nil
}

func (s *ShipmentService) GetTrackingEvents(shipmentID string) ([]*models.TrackingEvent, error) {
	events, ok := s.events[shipmentID]
	if !ok {
		return nil, fmt.Errorf("shipment not found: %s", shipmentID)
	}
	return events, nil
}

func (s *ShipmentService) CancelShipment(id string) (*models.Shipment, error) {
	shipment, ok := s.shipments[id]
	if !ok {
		return nil, fmt.Errorf("shipment not found: %s", id)
	}

	if shipment.Status != models.ShipmentStatusCreated {
		return nil, fmt.Errorf("can only cancel shipments in 'created' status")
	}

	shipment.Status = models.ShipmentStatusCancelled
	shipment.UpdatedAt = time.Now()
	s.addEvent(id, "cancelled", "", "Shipment cancelled")

	return shipment, nil
}

func (s *ShipmentService) addEvent(shipmentID, status, location, description string) {
	event := &models.TrackingEvent{
		ID:          uuid.New().String(),
		ShipmentID:  shipmentID,
		Status:      status,
		Location:    location,
		Description: description,
		Timestamp:   time.Now(),
	}
	s.events[shipmentID] = append(s.events[shipmentID], event)
}

func generateTrackingNumber(carrierCode string) string {
	return fmt.Sprintf("%s-%s", carrierCode, uuid.New().String()[:12])
}

