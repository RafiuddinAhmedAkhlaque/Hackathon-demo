package com.ecommerce.order.service;

import com.ecommerce.order.dto.OrderDTO;
import com.ecommerce.order.model.Order;
import com.ecommerce.order.model.OrderStatus;
import com.ecommerce.order.repository.OrderRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class OrderStatusServiceTest {
    private OrderStatusService statusService;
    private OrderService orderService;
    private OrderRepository orderRepository;

    @BeforeEach
    void setUp() {
        orderRepository = new OrderRepository();
        orderService = new OrderService(orderRepository);
        statusService = new OrderStatusService(orderRepository);
    }

    private Order createTestOrder() {
        OrderDTO dto = new OrderDTO();
        dto.setUserId("user-123");
        dto.setShippingAddressId("addr-456");
        dto.setItems(Arrays.asList(
                new OrderDTO.OrderItemDTO("prod-1", "Widget", "W-001", 1, 10.00)
        ));
        return orderService.createOrder(dto);
    }

    @Test
    void shouldUpdateStatusWithHistory() {
        Order order = createTestOrder();
        statusService.updateStatus(order.getId(), OrderStatus.CONFIRMED, "Payment received");
        List<OrderStatusService.StatusHistoryEntry> history = statusService.getStatusHistory(order.getId());
        assertEquals(1, history.size());
        assertEquals(OrderStatus.PENDING, history.get(0).getFromStatus());
        assertEquals(OrderStatus.CONFIRMED, history.get(0).getToStatus());
        assertEquals("Payment received", history.get(0).getReason());
    }

    @Test
    void shouldTrackMultipleTransitions() {
        Order order = createTestOrder();
        statusService.updateStatus(order.getId(), OrderStatus.CONFIRMED, "Payment OK");
        statusService.updateStatus(order.getId(), OrderStatus.PROCESSING, "Started processing");
        List<OrderStatusService.StatusHistoryEntry> history = statusService.getStatusHistory(order.getId());
        assertEquals(2, history.size());
    }

    @Test
    void shouldRejectInvalidTransition() {
        Order order = createTestOrder();
        assertThrows(IllegalStateException.class,
                () -> statusService.updateStatus(order.getId(), OrderStatus.SHIPPED, "Try to skip"));
    }

    @Test
    void shouldGetCurrentStatus() {
        Order order = createTestOrder();
        assertEquals(OrderStatus.PENDING, statusService.getCurrentStatus(order.getId()));
    }

    @Test
    void shouldCheckTransitionValidity() {
        Order order = createTestOrder();
        assertTrue(statusService.canTransition(order.getId(), OrderStatus.CONFIRMED));
        assertFalse(statusService.canTransition(order.getId(), OrderStatus.SHIPPED));
    }

    @Test
    void shouldReturnAvailableTransitions() {
        Order order = createTestOrder();
        List<OrderStatus> available = statusService.getAvailableTransitions(order.getId());
        assertTrue(available.contains(OrderStatus.CONFIRMED));
        assertTrue(available.contains(OrderStatus.CANCELLED));
        assertFalse(available.contains(OrderStatus.SHIPPED));
    }

    @Test
    void shouldReturnEmptyTransitionsForTerminalState() {
        Order order = createTestOrder();
        statusService.updateStatus(order.getId(), OrderStatus.CANCELLED, "Cancelled");
        List<OrderStatus> available = statusService.getAvailableTransitions(order.getId());
        assertTrue(available.isEmpty());
    }

    @Test
    void shouldThrowForNonexistentOrder() {
        assertThrows(IllegalArgumentException.class,
                () -> statusService.getCurrentStatus("nonexistent"));
    }
}

