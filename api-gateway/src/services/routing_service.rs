use crate::config::{GatewayConfig, RouteConfig};

pub struct RoutingService {
    config: GatewayConfig,
}

#[derive(Debug)]
pub struct ResolvedRoute {
    pub upstream_url: String,
    pub service_name: String,
    pub requires_auth: bool,
    pub upstream_path: String,
}

impl RoutingService {
    pub fn new(config: GatewayConfig) -> Self {
        Self { config }
    }

    pub fn resolve_route(&self, path: &str) -> Option<ResolvedRoute> {
        for route in &self.config.routes {
            if route.matches(path) {
                let upstream_path = path.strip_prefix(&route.path_prefix)
                    .unwrap_or("")
                    .to_string();

                return Some(ResolvedRoute {
                    upstream_url: format!("{}{}", route.upstream_url, upstream_path),
                    service_name: route.service_name.clone(),
                    requires_auth: route.requires_auth,
                    upstream_path,
                });
            }
        }
        None
    }

    pub fn list_routes(&self) -> &[RouteConfig] {
        &self.config.routes
    }

    pub fn get_active_routes(&self) -> Vec<&RouteConfig> {
        self.config.routes.iter().filter(|r| r.is_active).collect()
    }

    pub fn get_service_url(&self, service_name: &str) -> Option<String> {
        self.config.routes.iter()
            .find(|r| r.service_name == service_name)
            .map(|r| r.upstream_url.clone())
    }

    pub fn is_method_allowed(&self, path: &str, method: &str) -> bool {
        for route in &self.config.routes {
            if route.matches(path) {
                return route.methods.iter().any(|m| m == method);
            }
        }
        false
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn create_routing_service() -> RoutingService {
        RoutingService::new(GatewayConfig::default())
    }

    #[test]
    fn test_resolve_users_route() {
        let service = create_routing_service();
        let result = service.resolve_route("/users/123");
        assert!(result.is_some());
        let resolved = result.unwrap();
        assert_eq!(resolved.service_name, "user-service");
        assert!(resolved.upstream_url.contains("8001"));
    }

    #[test]
    fn test_resolve_products_route() {
        let service = create_routing_service();
        let result = service.resolve_route("/products");
        assert!(result.is_some());
        assert_eq!(result.unwrap().service_name, "product-service");
    }

    #[test]
    fn test_resolve_unknown_route() {
        let service = create_routing_service();
        let result = service.resolve_route("/unknown");
        assert!(result.is_none());
    }

    #[test]
    fn test_list_all_routes() {
        let service = create_routing_service();
        assert_eq!(service.list_routes().len(), 9);
    }

    #[test]
    fn test_get_active_routes() {
        let service = create_routing_service();
        let active = service.get_active_routes();
        assert_eq!(active.len(), 9);
    }

    #[test]
    fn test_get_service_url() {
        let service = create_routing_service();
        let url = service.get_service_url("user-service");
        assert!(url.is_some());
        assert!(url.unwrap().contains("8001"));
    }

    #[test]
    fn test_get_nonexistent_service_url() {
        let service = create_routing_service();
        let url = service.get_service_url("nonexistent");
        assert!(url.is_none());
    }

    #[test]
    fn test_method_allowed() {
        let service = create_routing_service();
        assert!(service.is_method_allowed("/users", "GET"));
        assert!(service.is_method_allowed("/users", "POST"));
    }

    #[test]
    fn test_method_not_allowed_unknown_path() {
        let service = create_routing_service();
        assert!(!service.is_method_allowed("/unknown", "GET"));
    }
}

