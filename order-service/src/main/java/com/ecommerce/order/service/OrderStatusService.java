package com.ecommerce.order.service;

import com.ecommerce.order.model.Order;
import com.ecommerce.order.model.OrderStatus;
import com.ecommerce.order.repository.OrderRepository;

import java.time.LocalDateTime;
import java.util.*;

public class OrderStatusService {
    private final OrderRepository orderRepository;
    private final Map<String, List<StatusHistoryEntry>> statusHistory = new HashMap<>();

    public OrderStatusService(OrderRepository orderRepository) {
        this.orderRepository = orderRepository;
    }

    public Order updateStatus(String orderId, OrderStatus newStatus, String reason) {
        Order order = orderRepository.findById(orderId)
                .orElseThrow(() -> new IllegalArgumentException("Order not found: " + orderId));

        OrderStatus oldStatus = order.getStatus();
        if (!oldStatus.canTransitionTo(newStatus)) {
            throw new IllegalStateException(
                    String.format("Invalid status transition from %s to %s", oldStatus, newStatus)
            );
        }

        // Record history
        StatusHistoryEntry entry = new StatusHistoryEntry(oldStatus, newStatus, reason);
        statusHistory.computeIfAbsent(orderId, k -> new ArrayList<>()).add(entry);

        order.setStatus(newStatus);
        return orderRepository.save(order);
    }

    public List<StatusHistoryEntry> getStatusHistory(String orderId) {
        return statusHistory.getOrDefault(orderId, Collections.emptyList());
    }

    public OrderStatus getCurrentStatus(String orderId) {
        return orderRepository.findById(orderId)
                .map(Order::getStatus)
                .orElseThrow(() -> new IllegalArgumentException("Order not found: " + orderId));
    }

    public boolean canTransition(String orderId, OrderStatus targetStatus) {
        return orderRepository.findById(orderId)
                .map(order -> order.getStatus().canTransitionTo(targetStatus))
                .orElse(false);
    }

    public List<OrderStatus> getAvailableTransitions(String orderId) {
        Order order = orderRepository.findById(orderId)
                .orElseThrow(() -> new IllegalArgumentException("Order not found: " + orderId));

        List<OrderStatus> available = new ArrayList<>();
        for (OrderStatus status : OrderStatus.values()) {
            if (order.getStatus().canTransitionTo(status)) {
                available.add(status);
            }
        }
        return available;
    }

    public static class StatusHistoryEntry {
        private final OrderStatus fromStatus;
        private final OrderStatus toStatus;
        private final String reason;
        private final LocalDateTime timestamp;

        public StatusHistoryEntry(OrderStatus fromStatus, OrderStatus toStatus, String reason) {
            this.fromStatus = fromStatus;
            this.toStatus = toStatus;
            this.reason = reason;
            this.timestamp = LocalDateTime.now();
        }

        public OrderStatus getFromStatus() { return fromStatus; }
        public OrderStatus getToStatus() { return toStatus; }
        public String getReason() { return reason; }
        public LocalDateTime getTimestamp() { return timestamp; }
    }
}

