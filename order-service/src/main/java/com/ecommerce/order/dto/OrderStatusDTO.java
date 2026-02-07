package com.ecommerce.order.dto;

import com.ecommerce.order.model.OrderStatus;

public class OrderStatusDTO {
    private String orderId;
    private OrderStatus currentStatus;
    private OrderStatus newStatus;
    private String reason;

    public OrderStatusDTO() {}

    public OrderStatusDTO(String orderId, OrderStatus newStatus, String reason) {
        this.orderId = orderId;
        this.newStatus = newStatus;
        this.reason = reason;
    }

    public String getOrderId() { return orderId; }
    public void setOrderId(String orderId) { this.orderId = orderId; }

    public OrderStatus getCurrentStatus() { return currentStatus; }
    public void setCurrentStatus(OrderStatus currentStatus) { this.currentStatus = currentStatus; }

    public OrderStatus getNewStatus() { return newStatus; }
    public void setNewStatus(OrderStatus newStatus) { this.newStatus = newStatus; }

    public String getReason() { return reason; }
    public void setReason(String reason) { this.reason = reason; }
}

