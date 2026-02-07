use serde::Serialize;

#[derive(Debug, Serialize)]
pub struct GatewayError {
    pub code: u16,
    pub message: String,
    pub error_type: GatewayErrorType,
}

#[derive(Debug, Serialize)]
pub enum GatewayErrorType {
    NotFound,
    Unauthorized,
    RateLimited,
    BadGateway,
    InternalError,
    MethodNotAllowed,
}

impl GatewayError {
    pub fn not_found(path: &str) -> Self {
        Self {
            code: 404,
            message: format!("No route found for path: {}", path),
            error_type: GatewayErrorType::NotFound,
        }
    }

    pub fn unauthorized(message: &str) -> Self {
        Self {
            code: 401,
            message: message.to_string(),
            error_type: GatewayErrorType::Unauthorized,
        }
    }

    pub fn rate_limited() -> Self {
        Self {
            code: 429,
            message: "Rate limit exceeded. Please try again later.".to_string(),
            error_type: GatewayErrorType::RateLimited,
        }
    }

    pub fn bad_gateway(service: &str) -> Self {
        Self {
            code: 502,
            message: format!("Service '{}' is unavailable", service),
            error_type: GatewayErrorType::BadGateway,
        }
    }

    pub fn internal(message: &str) -> Self {
        Self {
            code: 500,
            message: message.to_string(),
            error_type: GatewayErrorType::InternalError,
        }
    }

    pub fn method_not_allowed(method: &str, path: &str) -> Self {
        Self {
            code: 405,
            message: format!("Method '{}' not allowed for path: {}", method, path),
            error_type: GatewayErrorType::MethodNotAllowed,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_not_found_error() {
        let err = GatewayError::not_found("/test");
        assert_eq!(err.code, 404);
        assert!(err.message.contains("/test"));
    }

    #[test]
    fn test_unauthorized_error() {
        let err = GatewayError::unauthorized("No token");
        assert_eq!(err.code, 401);
    }

    #[test]
    fn test_rate_limited_error() {
        let err = GatewayError::rate_limited();
        assert_eq!(err.code, 429);
    }

    #[test]
    fn test_bad_gateway_error() {
        let err = GatewayError::bad_gateway("user-service");
        assert_eq!(err.code, 502);
        assert!(err.message.contains("user-service"));
    }

    #[test]
    fn test_method_not_allowed_error() {
        let err = GatewayError::method_not_allowed("DELETE", "/health");
        assert_eq!(err.code, 405);
    }
}

