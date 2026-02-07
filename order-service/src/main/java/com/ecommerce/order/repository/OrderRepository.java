package com.ecommerce.order.repository;

import com.ecommerce.order.model.Order;
import com.ecommerce.order.model.OrderStatus;

import java.util.*;
import java.util.stream.Collectors;

public class OrderRepository {
    private final Map<String, Order> orders = new HashMap<>();
    private final Map<String, List<String>> userOrders = new HashMap<>(); // userId -> orderIds

    public Order save(Order order) {
        orders.put(order.getId(), order);
        userOrders.computeIfAbsent(order.getUserId(), k -> new ArrayList<>());
        if (!userOrders.get(order.getUserId()).contains(order.getId())) {
            userOrders.get(order.getUserId()).add(order.getId());
        }
        return order;
    }

    public Optional<Order> findById(String id) {
        return Optional.ofNullable(orders.get(id));
    }

    public List<Order> findByUserId(String userId) {
        List<String> orderIds = userOrders.getOrDefault(userId, Collections.emptyList());
        return orderIds.stream()
                .map(orders::get)
                .filter(Objects::nonNull)
                .collect(Collectors.toList());
    }

    public List<Order> findByStatus(OrderStatus status) {
        return orders.values().stream()
                .filter(o -> o.getStatus() == status)
                .collect(Collectors.toList());
    }

    public List<Order> findAll(int skip, int limit) {
        return orders.values().stream()
                .skip(skip)
                .limit(limit)
                .collect(Collectors.toList());
    }

    public boolean delete(String id) {
        Order order = orders.remove(id);
        if (order != null) {
            List<String> userOrderIds = userOrders.get(order.getUserId());
            if (userOrderIds != null) {
                userOrderIds.remove(id);
            }
            return true;
        }
        return false;
    }

    public long count() {
        return orders.size();
    }
}

