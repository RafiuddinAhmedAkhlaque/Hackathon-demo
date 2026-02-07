package com.ecommerce.order.service;

import com.ecommerce.order.dto.CartDTO;
import com.ecommerce.order.model.Cart;
import com.ecommerce.order.model.CartItem;
import com.ecommerce.order.repository.CartRepository;

import java.util.Optional;

public class CartService {
    private final CartRepository cartRepository;

    public CartService(CartRepository cartRepository) {
        this.cartRepository = cartRepository;
    }

    public Cart getOrCreateCart(String userId) {
        if (userId == null || userId.isBlank()) {
            throw new IllegalArgumentException("User ID is required");
        }
        return cartRepository.getOrCreateForUser(userId);
    }

    public Cart addToCart(String userId, CartDTO cartDTO) {
        validateCartDTO(cartDTO);

        Cart cart = cartRepository.getOrCreateForUser(userId);
        CartItem item = new CartItem(
                cartDTO.getProductId(),
                cartDTO.getProductName(),
                cartDTO.getSku(),
                cartDTO.getQuantity(),
                cartDTO.getUnitPrice()
        );
        cart.addItem(item);
        return cartRepository.save(cart);
    }

    public Cart removeFromCart(String userId, String productId) {
        Cart cart = cartRepository.getOrCreateForUser(userId);
        boolean removed = cart.removeItem(productId);
        if (!removed) {
            throw new IllegalArgumentException("Product not found in cart: " + productId);
        }
        return cartRepository.save(cart);
    }

    public Cart updateQuantity(String userId, String productId, int quantity) {
        if (quantity < 0) {
            throw new IllegalArgumentException("Quantity cannot be negative");
        }

        Cart cart = cartRepository.getOrCreateForUser(userId);
        boolean updated = cart.updateItemQuantity(productId, quantity);
        if (!updated) {
            throw new IllegalArgumentException("Product not found in cart: " + productId);
        }
        return cartRepository.save(cart);
    }

    public Cart clearCart(String userId) {
        Cart cart = cartRepository.getOrCreateForUser(userId);
        cart.clear();
        return cartRepository.save(cart);
    }

    public Optional<Cart> getCart(String userId) {
        return cartRepository.findByUserId(userId);
    }

    public int getCartItemCount(String userId) {
        return cartRepository.findByUserId(userId)
                .map(Cart::getItemCount)
                .orElse(0);
    }

    public double getCartTotal(String userId) {
        return cartRepository.findByUserId(userId)
                .map(Cart::getTotalAmount)
                .orElse(0.0);
    }

    private void validateCartDTO(CartDTO dto) {
        if (dto.getProductId() == null || dto.getProductId().isBlank()) {
            throw new IllegalArgumentException("Product ID is required");
        }
        if (dto.getQuantity() <= 0) {
            throw new IllegalArgumentException("Quantity must be greater than zero");
        }
        if (dto.getUnitPrice() < 0) {
            throw new IllegalArgumentException("Unit price cannot be negative");
        }
    }
}

