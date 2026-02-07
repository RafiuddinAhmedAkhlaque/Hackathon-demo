package com.ecommerce.order.model;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

public class Order {
    private String id;
    private String userId;
    private List<OrderItem> items;
    private OrderStatus status;
    private double subtotal;
    private double taxAmount;
    private double shippingAmount;
    private double totalAmount;
    private String shippingAddressId;
    private String billingAddressId;
    private String notes;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    public Order() {
        this.id = UUID.randomUUID().toString();
        this.items = new ArrayList<>();
        this.status = OrderStatus.PENDING;
        this.createdAt = LocalDateTime.now();
        this.updatedAt = LocalDateTime.now();
    }

    public Order(String userId, String shippingAddressId) {
        this();
        this.userId = userId;
        this.shippingAddressId = shippingAddressId;
    }

    // Getters and setters
    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public String getUserId() { return userId; }
    public void setUserId(String userId) { this.userId = userId; }

    public List<OrderItem> getItems() { return items; }
    public void setItems(List<OrderItem> items) { this.items = items; }

    public OrderStatus getStatus() { return status; }
    public void setStatus(OrderStatus status) {
        this.status = status;
        this.updatedAt = LocalDateTime.now();
    }

    public double getSubtotal() { return subtotal; }
    public void setSubtotal(double subtotal) { this.subtotal = subtotal; }

    public double getTaxAmount() { return taxAmount; }
    public void setTaxAmount(double taxAmount) { this.taxAmount = taxAmount; }

    public double getShippingAmount() { return shippingAmount; }
    public void setShippingAmount(double shippingAmount) { this.shippingAmount = shippingAmount; }

    public double getTotalAmount() { return totalAmount; }
    public void setTotalAmount(double totalAmount) { this.totalAmount = totalAmount; }

    public String getShippingAddressId() { return shippingAddressId; }
    public void setShippingAddressId(String shippingAddressId) { this.shippingAddressId = shippingAddressId; }

    public String getBillingAddressId() { return billingAddressId; }
    public void setBillingAddressId(String billingAddressId) { this.billingAddressId = billingAddressId; }

    public String getNotes() { return notes; }
    public void setNotes(String notes) { this.notes = notes; }

    public LocalDateTime getCreatedAt() { return createdAt; }
    public LocalDateTime getUpdatedAt() { return updatedAt; }
    public void setUpdatedAt(LocalDateTime updatedAt) { this.updatedAt = updatedAt; }

    public void addItem(OrderItem item) {
        this.items.add(item);
        recalculateTotals();
    }

    public void removeItem(String itemId) {
        this.items.removeIf(item -> item.getId().equals(itemId));
        recalculateTotals();
    }

    public void recalculateTotals() {
        this.subtotal = items.stream()
                .mapToDouble(OrderItem::getLineTotal)
                .sum();
        this.subtotal = Math.round(this.subtotal * 100.0) / 100.0;
        this.totalAmount = Math.round((this.subtotal + this.taxAmount + this.shippingAmount) * 100.0) / 100.0;
    }
}

