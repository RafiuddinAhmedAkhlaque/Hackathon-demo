use std::collections::HashMap;
use std::time::{Duration, Instant};

/// Token bucket rate limiter
pub struct RateLimiter {
    requests_per_minute: u32,
    burst_size: u32,
    buckets: HashMap<String, TokenBucket>,
}

struct TokenBucket {
    tokens: f64,
    max_tokens: f64,
    refill_rate: f64, // tokens per second
    last_refill: Instant,
}

impl TokenBucket {
    fn new(max_tokens: f64, refill_rate: f64) -> Self {
        Self {
            tokens: max_tokens,
            max_tokens,
            refill_rate,
            last_refill: Instant::now(),
        }
    }

    fn try_consume(&mut self) -> bool {
        self.refill();
        if self.tokens >= 1.0 {
            self.tokens -= 1.0;
            true
        } else {
            false
        }
    }

    fn refill(&mut self) {
        let now = Instant::now();
        let elapsed = now.duration_since(self.last_refill).as_secs_f64();
        self.tokens = (self.tokens + elapsed * self.refill_rate).min(self.max_tokens);
        self.last_refill = now;
    }

    fn remaining_tokens(&mut self) -> u32 {
        self.refill();
        self.tokens as u32
    }
}

impl RateLimiter {
    pub fn new(requests_per_minute: u32, burst_size: u32) -> Self {
        Self {
            requests_per_minute,
            burst_size,
            buckets: HashMap::new(),
        }
    }

    /// Check if a request from the given client should be allowed
    pub fn allow_request(&mut self, client_id: &str) -> RateLimitResult {
        let bucket = self.buckets.entry(client_id.to_string()).or_insert_with(|| {
            TokenBucket::new(
                self.burst_size as f64,
                self.requests_per_minute as f64 / 60.0,
            )
        });

        let allowed = bucket.try_consume();
        let remaining = bucket.remaining_tokens();

        RateLimitResult {
            allowed,
            remaining,
            limit: self.requests_per_minute,
            reset_seconds: if allowed { 0 } else { 60 / self.requests_per_minute.max(1) },
        }
    }

    /// Get the number of tracked clients
    pub fn client_count(&self) -> usize {
        self.buckets.len()
    }

    /// Remove expired/inactive client buckets
    pub fn cleanup(&mut self, max_age: Duration) {
        let now = Instant::now();
        self.buckets.retain(|_, bucket| {
            now.duration_since(bucket.last_refill) < max_age
        });
    }
}

#[derive(Debug)]
pub struct RateLimitResult {
    pub allowed: bool,
    pub remaining: u32,
    pub limit: u32,
    pub reset_seconds: u32,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_allows_requests_within_limit() {
        let mut limiter = RateLimiter::new(60, 10);
        for _ in 0..10 {
            let result = limiter.allow_request("client-1");
            assert!(result.allowed);
        }
    }

    #[test]
    fn test_blocks_requests_over_burst() {
        let mut limiter = RateLimiter::new(60, 5);
        for _ in 0..5 {
            limiter.allow_request("client-1");
        }
        let result = limiter.allow_request("client-1");
        assert!(!result.allowed);
    }

    #[test]
    fn test_different_clients_independent() {
        let mut limiter = RateLimiter::new(60, 2);
        limiter.allow_request("client-1");
        limiter.allow_request("client-1");
        // Client-1 is at limit, but client-2 should still be allowed
        let result = limiter.allow_request("client-2");
        assert!(result.allowed);
    }

    #[test]
    fn test_remaining_tokens_reported() {
        let mut limiter = RateLimiter::new(60, 10);
        let result = limiter.allow_request("client-1");
        assert!(result.remaining <= 10);
    }

    #[test]
    fn test_client_count() {
        let mut limiter = RateLimiter::new(60, 10);
        limiter.allow_request("client-1");
        limiter.allow_request("client-2");
        assert_eq!(limiter.client_count(), 2);
    }

    #[test]
    fn test_cleanup_removes_old_entries() {
        let mut limiter = RateLimiter::new(60, 10);
        limiter.allow_request("client-1");
        // Cleanup with zero duration should remove all
        limiter.cleanup(Duration::from_secs(0));
        assert_eq!(limiter.client_count(), 0);
    }
}

