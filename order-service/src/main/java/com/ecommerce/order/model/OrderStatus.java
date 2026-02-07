package com.ecommerce.order.model;

public enum OrderStatus {
    PENDING,
    CONFIRMED,
    PROCESSING,
    SHIPPED,
    DELIVERED,
    CANCELLED,
    REFUNDED,
    ON_HOLD;

    /**
     * Check if transition to another status is valid.
     */
    public boolean canTransitionTo(OrderStatus target) {
        switch (this) {
            case PENDING:
                return target == CONFIRMED || target == CANCELLED;
            case CONFIRMED:
                return target == PROCESSING || target == CANCELLED || target == ON_HOLD;
            case PROCESSING:
                return target == SHIPPED || target == CANCELLED || target == ON_HOLD;
            case SHIPPED:
                return target == DELIVERED;
            case DELIVERED:
                return target == REFUNDED;
            case ON_HOLD:
                return target == PROCESSING || target == CANCELLED;
            case CANCELLED:
            case REFUNDED:
                return false; // Terminal states
            default:
                return false;
        }
    }
}

