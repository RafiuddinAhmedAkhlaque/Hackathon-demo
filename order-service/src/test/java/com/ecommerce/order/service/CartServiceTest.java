package com.ecommerce.order.service;

import com.ecommerce.order.dto.CartDTO;
import com.ecommerce.order.model.Cart;
import com.ecommerce.order.repository.CartRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Nested;

import static org.junit.jupiter.api.Assertions.*;

class CartServiceTest {
    private CartService cartService;
    private CartRepository cartRepository;

    @BeforeEach
    void setUp() {
        cartRepository = new CartRepository();
        cartService = new CartService(cartRepository);
    }

    private CartDTO createCartDTO(String productId, int quantity, double price) {
        return new CartDTO(productId, "Product " + productId, "SKU-" + productId, quantity, price);
    }

    @Nested
    class GetOrCreateCartTests {
        @Test
        void shouldCreateNewCartForUser() {
            Cart cart = cartService.getOrCreateCart("user-1");
            assertNotNull(cart);
            assertEquals("user-1", cart.getUserId());
            assertTrue(cart.isEmpty());
        }

        @Test
        void shouldReturnExistingCart() {
            Cart first = cartService.getOrCreateCart("user-1");
            Cart second = cartService.getOrCreateCart("user-1");
            assertEquals(first.getId(), second.getId());
        }

        @Test
        void shouldRejectNullUserId() {
            assertThrows(IllegalArgumentException.class, () -> cartService.getOrCreateCart(null));
        }
    }

    @Nested
    class AddToCartTests {
        @Test
        void shouldAddItemToCart() {
            Cart cart = cartService.addToCart("user-1", createCartDTO("prod-1", 2, 10.00));
            assertEquals(1, cart.getItems().size());
            assertEquals(2, cart.getItemCount());
            assertEquals(20.00, cart.getTotalAmount(), 0.01);
        }

        @Test
        void shouldMergeQuantityForSameProduct() {
            cartService.addToCart("user-1", createCartDTO("prod-1", 2, 10.00));
            Cart cart = cartService.addToCart("user-1", createCartDTO("prod-1", 3, 10.00));
            assertEquals(1, cart.getItems().size());
            assertEquals(5, cart.getItemCount());
        }

        @Test
        void shouldAddMultipleDifferentProducts() {
            cartService.addToCart("user-1", createCartDTO("prod-1", 1, 10.00));
            Cart cart = cartService.addToCart("user-1", createCartDTO("prod-2", 1, 20.00));
            assertEquals(2, cart.getItems().size());
            assertEquals(30.00, cart.getTotalAmount(), 0.01);
        }

        @Test
        void shouldRejectZeroQuantity() {
            assertThrows(IllegalArgumentException.class,
                    () -> cartService.addToCart("user-1", createCartDTO("prod-1", 0, 10.00)));
        }

        @Test
        void shouldRejectNegativePrice() {
            assertThrows(IllegalArgumentException.class,
                    () -> cartService.addToCart("user-1", createCartDTO("prod-1", 1, -5.00)));
        }
    }

    @Nested
    class RemoveFromCartTests {
        @Test
        void shouldRemoveItemFromCart() {
            cartService.addToCart("user-1", createCartDTO("prod-1", 2, 10.00));
            cartService.addToCart("user-1", createCartDTO("prod-2", 1, 20.00));
            Cart cart = cartService.removeFromCart("user-1", "prod-1");
            assertEquals(1, cart.getItems().size());
            assertEquals(20.00, cart.getTotalAmount(), 0.01);
        }

        @Test
        void shouldThrowForNonexistentProduct() {
            cartService.getOrCreateCart("user-1");
            assertThrows(IllegalArgumentException.class,
                    () -> cartService.removeFromCart("user-1", "nonexistent"));
        }
    }

    @Nested
    class UpdateQuantityTests {
        @Test
        void shouldUpdateItemQuantity() {
            cartService.addToCart("user-1", createCartDTO("prod-1", 2, 10.00));
            Cart cart = cartService.updateQuantity("user-1", "prod-1", 5);
            assertEquals(5, cart.getItemCount());
            assertEquals(50.00, cart.getTotalAmount(), 0.01);
        }

        @Test
        void shouldRemoveItemWhenQuantityIsZero() {
            cartService.addToCart("user-1", createCartDTO("prod-1", 2, 10.00));
            Cart cart = cartService.updateQuantity("user-1", "prod-1", 0);
            assertTrue(cart.isEmpty());
        }

        @Test
        void shouldRejectNegativeQuantity() {
            cartService.addToCart("user-1", createCartDTO("prod-1", 2, 10.00));
            assertThrows(IllegalArgumentException.class,
                    () -> cartService.updateQuantity("user-1", "prod-1", -1));
        }
    }

    @Nested
    class ClearCartTests {
        @Test
        void shouldClearAllItems() {
            cartService.addToCart("user-1", createCartDTO("prod-1", 2, 10.00));
            cartService.addToCart("user-1", createCartDTO("prod-2", 1, 20.00));
            Cart cart = cartService.clearCart("user-1");
            assertTrue(cart.isEmpty());
            assertEquals(0.00, cart.getTotalAmount(), 0.01);
        }
    }

    @Nested
    class CartQueryTests {
        @Test
        void shouldGetCartItemCount() {
            cartService.addToCart("user-1", createCartDTO("prod-1", 3, 10.00));
            cartService.addToCart("user-1", createCartDTO("prod-2", 2, 20.00));
            assertEquals(5, cartService.getCartItemCount("user-1"));
        }

        @Test
        void shouldReturnZeroCountForEmptyCart() {
            assertEquals(0, cartService.getCartItemCount("nonexistent-user"));
        }

        @Test
        void shouldGetCartTotal() {
            cartService.addToCart("user-1", createCartDTO("prod-1", 2, 10.00));
            cartService.addToCart("user-1", createCartDTO("prod-2", 1, 30.00));
            assertEquals(50.00, cartService.getCartTotal("user-1"), 0.01);
        }
    }
}

