package com.ecommerce.order.dto;

import java.util.List;

public class OrderDTO {
    private String userId;
    private List<OrderItemDTO> items;
    private String shippingAddressId;
    private String billingAddressId;
    private String notes;
    private double taxRate;
    private double shippingAmount;

    public OrderDTO() {}

    // Getters and setters
    public String getUserId() { return userId; }
    public void setUserId(String userId) { this.userId = userId; }

    public List<OrderItemDTO> getItems() { return items; }
    public void setItems(List<OrderItemDTO> items) { this.items = items; }

    public String getShippingAddressId() { return shippingAddressId; }
    public void setShippingAddressId(String shippingAddressId) { this.shippingAddressId = shippingAddressId; }

    public String getBillingAddressId() { return billingAddressId; }
    public void setBillingAddressId(String billingAddressId) { this.billingAddressId = billingAddressId; }

    public String getNotes() { return notes; }
    public void setNotes(String notes) { this.notes = notes; }

    public double getTaxRate() { return taxRate; }
    public void setTaxRate(double taxRate) { this.taxRate = taxRate; }

    public double getShippingAmount() { return shippingAmount; }
    public void setShippingAmount(double shippingAmount) { this.shippingAmount = shippingAmount; }

    public static class OrderItemDTO {
        private String productId;
        private String productName;
        private String sku;
        private int quantity;
        private double unitPrice;

        public OrderItemDTO() {}

        public OrderItemDTO(String productId, String productName, String sku, int quantity, double unitPrice) {
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
}

