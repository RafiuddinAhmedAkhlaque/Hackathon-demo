package com.ecommerce.order.dto;

public class CartDTO {
    private String productId;
    private String productName;
    private String sku;
    private int quantity;
    private double unitPrice;

    public CartDTO() {}

    public CartDTO(String productId, String productName, String sku, int quantity, double unitPrice) {
        this.productId = productId;
        this.productName = productName;
        this.sku = sku;
        this.quantity = quantity;
        this.unitPrice = unitPrice;
    }

    public String getProductId() { return productId; }
    public void setProductId(String productId) { this.productId = productId; }

    public String getProductName() { return productName; }
    public void setProductName(String productName) { this.productName = productName; }

    public String getSku() { return sku; }
    public void setSku(String sku) { this.sku = sku; }

    public int getQuantity() { return quantity; }
    public void setQuantity(int quantity) { this.quantity = quantity; }

    public double getUnitPrice() { return unitPrice; }
    public void setUnitPrice(double unitPrice) { this.unitPrice = unitPrice; }
}

