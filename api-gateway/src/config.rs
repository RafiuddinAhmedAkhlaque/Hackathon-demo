use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GatewayConfig {
    pub port: u16,
    pub routes: Vec<RouteConfig>,
    pub rate_limit: RateLimitConfig,
    pub cors: CorsConfig,
}

impl Default for GatewayConfig {
    fn default() -> Self {
        Self {
            port: 8000,
            routes: vec![
                RouteConfig::new("/users", "http://localhost:8001", "user-service"),
                RouteConfig::new("/products", "http://localhost:8002", "product-service"),
                RouteConfig::new("/orders", "http://localhost:8003", "order-service"),
                RouteConfig::new("/payments", "http://localhost:8004", "payment-service"),
                RouteConfig::new("/inventory", "http://localhost:8005", "inventory-service"),
                RouteConfig::new("/notifications", "http://localhost:8006", "notification-service"),
                RouteConfig::new("/shipping", "http://localhost:8007", "shipping-service"),
                RouteConfig::new("/analytics", "http://localhost:8008", "analytics-service"),
                RouteConfig::new("/reviews", "http://localhost:8009", "review-service"),
            ],
            rate_limit: RateLimitConfig::default(),
            cors: CorsConfig::default(),
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RouteConfig {
    pub path_prefix: String,
    pub upstream_url: String,
    pub service_name: String,
    pub requires_auth: bool,
    pub rate_limit_override: Option<u32>,
    pub methods: Vec<String>,
    pub is_active: bool,
}

impl RouteConfig {
    pub fn new(path_prefix: &str, upstream_url: &str, service_name: &str) -> Self {
        Self {
            path_prefix: path_prefix.to_string(),
            upstream_url: upstream_url.to_string(),
            service_name: service_name.to_string(),
            requires_auth: false,
            rate_limit_override: None,
            methods: vec!["GET".into(), "POST".into(), "PUT".into(), "DELETE".into()],
            is_active: true,
        }
    }

    pub fn with_auth(mut self) -> Self {
        self.requires_auth = true;
        self
    }

    pub fn matches(&self, path: &str) -> bool {
        self.is_active && path.starts_with(&self.path_prefix)
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RateLimitConfig {
    pub requests_per_minute: u32,
    pub burst_size: u32,
    pub enabled: bool,
}

impl Default for RateLimitConfig {
    fn default() -> Self {
        Self {
            requests_per_minute: 60,
            burst_size: 10,
            enabled: true,
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CorsConfig {
    pub allowed_origins: Vec<String>,
    pub allowed_methods: Vec<String>,
    pub allowed_headers: Vec<String>,
    pub max_age: u32,
}

impl Default for CorsConfig {
    fn default() -> Self {
        Self {
            allowed_origins: vec!["*".to_string()],
            allowed_methods: vec!["GET".into(), "POST".into(), "PUT".into(), "DELETE".into(), "OPTIONS".into()],
            allowed_headers: vec!["Content-Type".into(), "Authorization".into()],
            max_age: 3600,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_default_config_has_all_routes() {
        let config = GatewayConfig::default();
        assert_eq!(config.routes.len(), 9);
        assert_eq!(config.port, 8000);
    }

    #[test]
    fn test_route_config_matches() {
        let route = RouteConfig::new("/users", "http://localhost:8001", "user-service");
        assert!(route.matches("/users"));
        assert!(route.matches("/users/123"));
        assert!(!route.matches("/products"));
    }

    #[test]
    fn test_route_config_with_auth() {
        let route = RouteConfig::new("/orders", "http://localhost:8003", "order-service")
            .with_auth();
        assert!(route.requires_auth);
    }

    #[test]
    fn test_inactive_route_does_not_match() {
        let mut route = RouteConfig::new("/users", "http://localhost:8001", "user-service");
        route.is_active = false;
        assert!(!route.matches("/users"));
    }

    #[test]
    fn test_default_rate_limit() {
        let config = RateLimitConfig::default();
        assert_eq!(config.requests_per_minute, 60);
        assert!(config.enabled);
    }

    #[test]
    fn test_default_cors() {
        let cors = CorsConfig::default();
        assert!(cors.allowed_origins.contains(&"*".to_string()));
        assert_eq!(cors.max_age, 3600);
    }
}

