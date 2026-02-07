package services

import (
	"testing"

	"github.com/ecommerce/shipping-service/models"
)

func validShipmentRequest() CreateShipmentRequest {
	return CreateShipmentRequest{
		OrderID:     "order-123",
		CarrierCode: "fedex",
		ServiceType: "ground",
		FromAddress: models.Address{
			Name: "Warehouse", Street: "100 Industrial Way",
			City: "Newark", State: "NJ", PostalCode: "07101", Country: "US",
		},
		ToAddress: models.Address{
			Name: "Customer", Street: "200 Main St",
			City: "Los Angeles", State: "CA", PostalCode: "90001", Country: "US",
		},
		Weight:     3.5,
		Dimensions: models.Dimensions{Length: 30, Width: 20, Height: 15, Unit: "cm"},
	}
}

func TestCreateShipment_Success(t *testing.T) {
	service := NewShipmentService()
	shipment, err := service.CreateShipment(validShipmentRequest())

	if err != nil {
		t.Fatalf("expected no error, got %v", err)
	}
	if shipment.ID == "" {
		t.Error("expected shipment ID to be set")
	}
	if shipment.TrackingNumber == "" {
		t.Error("expected tracking number to be set")
	}
	if shipment.Status != models.ShipmentStatusCreated {
		t.Errorf("expected status 'created', got '%s'", shipment.Status)
	}
}

func TestCreateShipment_MissingOrderID(t *testing.T) {
	service := NewShipmentService()
	req := validShipmentRequest()
	req.OrderID = ""

	_, err := service.CreateShipment(req)
	if err == nil {
		t.Error("expected error for missing order ID")
	}
}

func TestCreateShipment_InvalidCarrier(t *testing.T) {
	service := NewShipmentService()
	req := validShipmentRequest()
	req.CarrierCode = "nonexistent"

	_, err := service.CreateShipment(req)
	if err == nil {
		t.Error("expected error for invalid carrier")
	}
}

func TestGetShipment(t *testing.T) {
	service := NewShipmentService()
	created, _ := service.CreateShipment(validShipmentRequest())

	found, err := service.GetShipment(created.ID)
	if err != nil {
		t.Fatalf("expected no error, got %v", err)
	}
	if found.ID != created.ID {
		t.Errorf("expected ID %s, got %s", created.ID, found.ID)
	}
}

func TestGetShipment_NotFound(t *testing.T) {
	service := NewShipmentService()
	_, err := service.GetShipment("nonexistent")
	if err == nil {
		t.Error("expected error for nonexistent shipment")
	}
}

func TestUpdateStatus(t *testing.T) {
	service := NewShipmentService()
	shipment, _ := service.CreateShipment(validShipmentRequest())

	updated, err := service.UpdateStatus(shipment.ID, models.ShipmentStatusInTransit, "Newark, NJ", "Package in transit")
	if err != nil {
		t.Fatalf("expected no error, got %v", err)
	}
	if updated.Status != models.ShipmentStatusInTransit {
		t.Errorf("expected status 'in_transit', got '%s'", updated.Status)
	}
}

func TestUpdateStatus_Delivered(t *testing.T) {
	service := NewShipmentService()
	shipment, _ := service.CreateShipment(validShipmentRequest())

	delivered, err := service.UpdateStatus(shipment.ID, models.ShipmentStatusDelivered, "Los Angeles, CA", "Package delivered")
	if err != nil {
		t.Fatalf("expected no error, got %v", err)
	}
	if delivered.ActualDelivery == nil {
		t.Error("expected actual delivery time to be set")
	}
}

func TestGetTrackingEvents(t *testing.T) {
	service := NewShipmentService()
	shipment, _ := service.CreateShipment(validShipmentRequest())
	service.UpdateStatus(shipment.ID, models.ShipmentStatusPickedUp, "Newark, NJ", "Picked up")
	service.UpdateStatus(shipment.ID, models.ShipmentStatusInTransit, "Philadelphia, PA", "In transit")

	events, err := service.GetTrackingEvents(shipment.ID)
	if err != nil {
		t.Fatalf("expected no error, got %v", err)
	}
	// Created + picked_up + in_transit = 3 events
	if len(events) != 3 {
		t.Errorf("expected 3 events, got %d", len(events))
	}
}

func TestCancelShipment(t *testing.T) {
	service := NewShipmentService()
	shipment, _ := service.CreateShipment(validShipmentRequest())

	cancelled, err := service.CancelShipment(shipment.ID)
	if err != nil {
		t.Fatalf("expected no error, got %v", err)
	}
	if cancelled.Status != models.ShipmentStatusCancelled {
		t.Errorf("expected status 'cancelled', got '%s'", cancelled.Status)
	}
}

func TestCancelShipment_NotCreatedStatus(t *testing.T) {
	service := NewShipmentService()
	shipment, _ := service.CreateShipment(validShipmentRequest())
	service.UpdateStatus(shipment.ID, models.ShipmentStatusInTransit, "City", "In transit")

	_, err := service.CancelShipment(shipment.ID)
	if err == nil {
		t.Error("expected error for cancelling non-created shipment")
	}
}

