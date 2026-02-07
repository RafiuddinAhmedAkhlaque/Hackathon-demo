package com.ecommerce.order.repository;

import com.ecommerce.order.model.Cart;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

public class CartRepository {
    private final Map<String, Cart> carts = new HashMap<>();
    private final Map<String, String> userCarts = new HashMap<>(); // userId -> cartId

    public Cart save(Cart cart) {
        carts.put(cart.getId(), cart);
        userCarts.put(cart.getUserId(), cart.getId());
        return cart;
    }

    public Optional<Cart> findById(String id) {
        return Optional.ofNullable(carts.get(id));
    }

    public Optional<Cart> findByUserId(String userId) {
        String cartId = userCarts.get(userId);
        if (cartId != null) {
            return Optional.ofNullable(carts.get(cartId));
        }
        return Optional.empty();
    }

    public Cart getOrCreateForUser(String userId) {
        Optional<Cart> existing = findByUserId(userId);
        if (existing.isPresent()) {
            return existing.get();
        }
        Cart cart = new Cart(userId);
        return save(cart);
    }

    public boolean delete(String id) {
        Cart cart = carts.remove(id);
        if (cart != null) {
            userCarts.remove(cart.getUserId());
            return true;
        }
        return false;
    }

    public boolean deleteByUserId(String userId) {
        String cartId = userCarts.remove(userId);
        if (cartId != null) {
            carts.remove(cartId);
            return true;
        }
        return false;
    }
}

