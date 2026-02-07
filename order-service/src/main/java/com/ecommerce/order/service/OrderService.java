package com.ecommerce.order.service;

import com.ecommerce.order.dto.OrderDTO;
import com.ecommerce.order.model.*;
import com.ecommerce.order.repository.OrderRepository;

import java.util.List;
import java.util.Optional;

public class OrderService {
    private final OrderRepository orderRepository;
    private static final double DEFAULT_TAX_RATE = 0.08; // 8%

    public OrderService(OrderRepository orderRepository) {
        this.orderRepository = orderRepository;
    }

    public Order createOrder(OrderDTO orderDTO) {
        validateOrderDTO(orderDTO);

        Order order = new Order(orderDTO.getUserId(), orderDTO.getShippingAddressId());
        order.setBillingAddressId(orderDTO.getBillingAddressId());
        order.setNotes(orderDTO.getNotes());

        // Add items
        for (OrderDTO.OrderItemDTO itemDTO : orderDTO.getItems()) {
            validateOrderItem(itemDTO);
            OrderItem item = new OrderItem(
                    itemDTO.getProductId(),
                    itemDTO.getProductName(),
                    itemDTO.getSku(),
                    itemDTO.getQuantity(),
                    itemDTO.getUnitPrice()
            );
            order.addItem(item);
        }

        // Calculate tax
        double taxRate = orderDTO.getTaxRate() > 0 ? orderDTO.getTaxRate() : DEFAULT_TAX_RATE;
        order.setTaxAmount(Math.round(order.getSubtotal() * taxRate * 100.0) / 100.0);
        order.setShippingAmount(orderDTO.getShippingAmount());
        order.recalculateTotals();

        return orderRepository.save(order);
    }

    public Optional<Order> getOrder(String orderId) {
        return orderRepository.findById(orderId);
    }

    public List<Order> getOrdersByUser(String userId) {
        return orderRepository.findByUserId(userId);
    }

    public List<Order> getOrdersByStatus(OrderStatus status) {
        return orderRepository.findByStatus(status);
    }

    public List<Order> listOrders(int skip, int limit) {
        return orderRepository.findAll(skip, limit);
    }

    public Order confirmOrder(String orderId) {
        return transitionStatus(orderId, OrderStatus.CONFIRMED);
    }

    public Order processOrder(String orderId) {
        return transitionStatus(orderId, OrderStatus.PROCESSING);
    }

    public Order shipOrder(String orderId) {
        return transitionStatus(orderId, OrderStatus.SHIPPED);
    }

    public Order deliverOrder(String orderId) {
        return transitionStatus(orderId, OrderStatus.DELIVERED);
    }

    public Order cancelOrder(String orderId, String reason) {
        Order order = transitionStatus(orderId, OrderStatus.CANCELLED);
        order.setNotes(reason);
        return orderRepository.save(order);
    }

    public Order holdOrder(String orderId, String reason) {
        Order order = transitionStatus(orderId, OrderStatus.ON_HOLD);
        order.setNotes(reason);
        return orderRepository.save(order);
    }

    public Order refundOrder(String orderId) {
        return transitionStatus(orderId, OrderStatus.REFUNDED);
    }

    public double calculateOrderTotal(String orderId) {
        Order order = orderRepository.findById(orderId)
                .orElseThrow(() -> new IllegalArgumentException("Order not found: " + orderId));
        return order.getTotalAmount();
    }

    public boolean deleteOrder(String orderId) {
        Order order = orderRepository.findById(orderId)
                .orElseThrow(() -> new IllegalArgumentException("Order not found: " + orderId));

        if (order.getStatus() != OrderStatus.PENDING && order.getStatus() != OrderStatus.CANCELLED) {
            throw new IllegalStateException("Can only delete orders in PENDING or CANCELLED status");
        }

        return orderRepository.delete(orderId);
    }

    private Order transitionStatus(String orderId, OrderStatus newStatus) {
        Order order = orderRepository.findById(orderId)
                .orElseThrow(() -> new IllegalArgumentException("Order not found: " + orderId));

        if (!order.getStatus().canTransitionTo(newStatus)) {
            throw new IllegalStateException(
                    String.format("Cannot transition from %s to %s", order.getStatus(), newStatus)
            );
        }

        order.setStatus(newStatus);
        return orderRepository.save(order);
    }

    private void validateOrderDTO(OrderDTO dto) {
        if (dto.getUserId() == null || dto.getUserId().isBlank()) {
            throw new IllegalArgumentException("User ID is required");
        }
        if (dto.getItems() == null || dto.getItems().isEmpty()) {
            throw new IllegalArgumentException("Order must have at least one item");
        }
        if (dto.getShippingAddressId() == null || dto.getShippingAddressId().isBlank()) {
            throw new IllegalArgumentException("Shipping address is required");
        }
    }

    private void validateOrderItem(OrderDTO.OrderItemDTO item) {
        if (item.getProductId() == null || item.getProductId().isBlank()) {
            throw new IllegalArgumentException("Product ID is required for order items");
        }
        if (item.getQuantity() <= 0) {
            throw new IllegalArgumentException("Quantity must be greater than zero");
        }
        if (item.getUnitPrice() < 0) {
            throw new IllegalArgumentException("Unit price cannot be negative");
        }
    }
}

