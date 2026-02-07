package com.ecommerce.order.service;

import com.ecommerce.order.dto.OrderDTO;
import com.ecommerce.order.model.Order;
import com.ecommerce.order.model.OrderStatus;
import com.ecommerce.order.repository.OrderRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Nested;

import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class OrderServiceTest {
    private OrderService orderService;
    private OrderRepository orderRepository;

    @BeforeEach
    void setUp() {
        orderRepository = new OrderRepository();
        orderService = new OrderService(orderRepository);
    }

    private OrderDTO createValidOrderDTO() {
        OrderDTO dto = new OrderDTO();
        dto.setUserId("user-123");
        dto.setShippingAddressId("addr-456");
        dto.setShippingAmount(9.99);
        dto.setItems(Arrays.asList(
                new OrderDTO.OrderItemDTO("prod-1", "Widget A", "WA-001", 2, 25.00),
                new OrderDTO.OrderItemDTO("prod-2", "Widget B", "WB-001", 1, 15.00)
        ));
        return dto;
    }

    @Nested
    class CreateOrderTests {
        @Test
        void shouldCreateOrderSuccessfully() {
            OrderDTO dto = createValidOrderDTO();
            Order order = orderService.createOrder(dto);

            assertNotNull(order.getId());
            assertEquals("user-123", order.getUserId());
            assertEquals(OrderStatus.PENDING, order.getStatus());
            assertEquals(2, order.getItems().size());
        }

        @Test
        void shouldCalculateSubtotalCorrectly() {
            OrderDTO dto = createValidOrderDTO();
            Order order = orderService.createOrder(dto);

            // 2 * 25.00 + 1 * 15.00 = 65.00
            assertEquals(65.00, order.getSubtotal(), 0.01);
        }

        @Test
        void shouldCalculateTaxCorrectly() {
            OrderDTO dto = createValidOrderDTO();
            Order order = orderService.createOrder(dto);

            // 65.00 * 0.08 = 5.20
            assertEquals(5.20, order.getTaxAmount(), 0.01);
        }

        @Test
        void shouldRejectMissingUserId() {
            OrderDTO dto = createValidOrderDTO();
            dto.setUserId(null);
            assertThrows(IllegalArgumentException.class, () -> orderService.createOrder(dto));
        }

        @Test
        void shouldRejectEmptyItems() {
            OrderDTO dto = createValidOrderDTO();
            dto.setItems(Arrays.asList());
            assertThrows(IllegalArgumentException.class, () -> orderService.createOrder(dto));
        }

        @Test
        void shouldRejectMissingShippingAddress() {
            OrderDTO dto = createValidOrderDTO();
            dto.setShippingAddressId(null);
            assertThrows(IllegalArgumentException.class, () -> orderService.createOrder(dto));
        }

        @Test
        void shouldRejectInvalidItemQuantity() {
            OrderDTO dto = createValidOrderDTO();
            dto.setItems(Arrays.asList(
                    new OrderDTO.OrderItemDTO("prod-1", "Widget", "W-001", 0, 10.00)
            ));
            assertThrows(IllegalArgumentException.class, () -> orderService.createOrder(dto));
        }
    }

    @Nested
    class StatusTransitionTests {
        @Test
        void shouldConfirmPendingOrder() {
            Order order = orderService.createOrder(createValidOrderDTO());
            Order confirmed = orderService.confirmOrder(order.getId());
            assertEquals(OrderStatus.CONFIRMED, confirmed.getStatus());
        }

        @Test
        void shouldProcessConfirmedOrder() {
            Order order = orderService.createOrder(createValidOrderDTO());
            orderService.confirmOrder(order.getId());
            Order processed = orderService.processOrder(order.getId());
            assertEquals(OrderStatus.PROCESSING, processed.getStatus());
        }

        @Test
        void shouldShipProcessedOrder() {
            Order order = orderService.createOrder(createValidOrderDTO());
            orderService.confirmOrder(order.getId());
            orderService.processOrder(order.getId());
            Order shipped = orderService.shipOrder(order.getId());
            assertEquals(OrderStatus.SHIPPED, shipped.getStatus());
        }

        @Test
        void shouldDeliverShippedOrder() {
            Order order = orderService.createOrder(createValidOrderDTO());
            orderService.confirmOrder(order.getId());
            orderService.processOrder(order.getId());
            orderService.shipOrder(order.getId());
            Order delivered = orderService.deliverOrder(order.getId());
            assertEquals(OrderStatus.DELIVERED, delivered.getStatus());
        }

        @Test
        void shouldNotSkipStatuses() {
            Order order = orderService.createOrder(createValidOrderDTO());
            assertThrows(IllegalStateException.class, () -> orderService.shipOrder(order.getId()));
        }

        @Test
        void shouldCancelPendingOrder() {
            Order order = orderService.createOrder(createValidOrderDTO());
            Order cancelled = orderService.cancelOrder(order.getId(), "Changed my mind");
            assertEquals(OrderStatus.CANCELLED, cancelled.getStatus());
        }

        @Test
        void shouldNotCancelDeliveredOrder() {
            Order order = orderService.createOrder(createValidOrderDTO());
            orderService.confirmOrder(order.getId());
            orderService.processOrder(order.getId());
            orderService.shipOrder(order.getId());
            orderService.deliverOrder(order.getId());
            assertThrows(IllegalStateException.class,
                    () -> orderService.cancelOrder(order.getId(), "Too late"));
        }

        @Test
        void shouldRefundDeliveredOrder() {
            Order order = orderService.createOrder(createValidOrderDTO());
            orderService.confirmOrder(order.getId());
            orderService.processOrder(order.getId());
            orderService.shipOrder(order.getId());
            orderService.deliverOrder(order.getId());
            Order refunded = orderService.refundOrder(order.getId());
            assertEquals(OrderStatus.REFUNDED, refunded.getStatus());
        }
    }

    @Nested
    class QueryTests {
        @Test
        void shouldFindOrderById() {
            Order order = orderService.createOrder(createValidOrderDTO());
            assertTrue(orderService.getOrder(order.getId()).isPresent());
        }

        @Test
        void shouldReturnEmptyForNonexistent() {
            assertTrue(orderService.getOrder("nonexistent").isEmpty());
        }

        @Test
        void shouldFindOrdersByUser() {
            orderService.createOrder(createValidOrderDTO());
            orderService.createOrder(createValidOrderDTO());
            List<Order> orders = orderService.getOrdersByUser("user-123");
            assertEquals(2, orders.size());
        }

        @Test
        void shouldFindOrdersByStatus() {
            orderService.createOrder(createValidOrderDTO());
            Order second = orderService.createOrder(createValidOrderDTO());
            orderService.confirmOrder(second.getId());
            List<Order> pending = orderService.getOrdersByStatus(OrderStatus.PENDING);
            assertEquals(1, pending.size());
        }
    }

    @Nested
    class DeleteTests {
        @Test
        void shouldDeletePendingOrder() {
            Order order = orderService.createOrder(createValidOrderDTO());
            assertTrue(orderService.deleteOrder(order.getId()));
        }

        @Test
        void shouldNotDeleteConfirmedOrder() {
            Order order = orderService.createOrder(createValidOrderDTO());
            orderService.confirmOrder(order.getId());
            assertThrows(IllegalStateException.class, () -> orderService.deleteOrder(order.getId()));
        }
    }
}

