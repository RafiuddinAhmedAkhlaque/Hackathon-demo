package com.ecommerce.order.model;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

public class Cart {
    private String id;
    private String userId;
    private List<CartItem> items;
    private double totalAmount;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;

    public Cart() {
        this.id = UUID.randomUUID().toString();
        this.items = new ArrayList<>();
        this.createdAt = LocalDateTime.now();
        this.updatedAt = LocalDateTime.now();
    }

    public Cart(String userId) {
        this();
        this.userId = userId;
    }

    // Getters and setters
    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public String getUserId() { return userId; }
    public void setUserId(String userId) { this.userId = userId; }

    public List<CartItem> getItems() { return items; }
    public void setItems(List<CartItem> items) { this.items = items; }

    public double getTotalAmount() { return totalAmount; }

    public LocalDateTime getCreatedAt() { return createdAt; }
    public LocalDateTime getUpdatedAt() { return updatedAt; }

    public void addItem(CartItem item) {
        Optional<CartItem> existing = items.stream()
                .filter(i -> i.getProductId().equals(item.getProductId()))
                .findFirst();

        if (existing.isPresent()) {
            existing.get().setQuantity(existing.get().getQuantity() + item.getQuantity());
        } else {
            items.add(item);
        }
        recalculateTotal();
    }

    public boolean removeItem(String productId) {
        boolean removed = items.removeIf(i -> i.getProductId().equals(productId));
        if (removed) {
            recalculateTotal();
        }
        return removed;
    }

    public boolean updateItemQuantity(String productId, int quantity) {
        Optional<CartItem> item = items.stream()
                .filter(i -> i.getProductId().equals(productId))
                .findFirst();

        if (item.isEmpty()) {
            return false;
        }

        if (quantity <= 0) {
            return removeItem(productId);
        }

        item.get().setQuantity(quantity);
        recalculateTotal();
        return true;
    }

    public void clear() {
        items.clear();
        totalAmount = 0;
        updatedAt = LocalDateTime.now();
    }

    public int getItemCount() {
        return items.stream().mapToInt(CartItem::getQuantity).sum();
    }

    public boolean isEmpty() {
        return items.isEmpty();
    }

    private void recalculateTotal() {
        this.totalAmount = items.stream()
                .mapToDouble(CartItem::getLineTotal)
                .sum();
        this.totalAmount = Math.round(this.totalAmount * 100.0) / 100.0;
        this.updatedAt = LocalDateTime.now();
    }
}

