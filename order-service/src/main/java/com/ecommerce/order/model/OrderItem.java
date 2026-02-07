package com.ecommerce.order.model;

import java.util.UUID;

public class OrderItem {
    private String id;
    private String productId;
    private String productName;
    private String sku;
    private int quantity;
    private double unitPrice;
    private double lineTotal;

    public OrderItem() {
        this.id = UUID.randomUUID().toString();
    }

    public OrderItem(String productId, String productName, String sku, int quantity, double unitPrice) {
        this();
        this.productId = productId;
        this.productName = productName;
        this.sku = sku;
        this.quantity = quantity;
        this.unitPrice = unitPrice;
        this.lineTotal = Math.round(quantity * unitPrice * 100.0) / 100.0;
    }

    // Getters and setters
    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public String getProductId() { return productId; }
    public void setProductId(String productId) { this.productId = productId; }

    public String getProductName() { return productName; }
    public void setProductName(String productName) { this.productName = productName; }

    public String getSku() { return sku; }
    public void setSku(String sku) { this.sku = sku; }

    public int getQuantity() { return quantity; }
    public void setQuantity(int quantity) {
        this.quantity = quantity;
        this.lineTotal = Math.round(quantity * unitPrice * 100.0) / 100.0;
    }

    public double getUnitPrice() { return unitPrice; }
    public void setUnitPrice(double unitPrice) {
        this.unitPrice = unitPrice;
        this.lineTotal = Math.round(quantity * unitPrice * 100.0) / 100.0;
    }

    public double getLineTotal() { return lineTotal; }
}

