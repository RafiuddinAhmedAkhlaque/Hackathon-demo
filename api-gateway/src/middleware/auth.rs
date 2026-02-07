use std::collections::HashMap;

/// Simple JWT-like auth middleware (mock implementation for gateway)
pub struct AuthMiddleware {
    /// Map of valid API keys to user info
    api_keys: HashMap<String, AuthInfo>,
    /// Paths that don't require authentication
    public_paths: Vec<String>,
}

#[derive(Debug, Clone)]
pub struct AuthInfo {
    pub user_id: String,
    pub roles: Vec<String>,
}

#[derive(Debug)]
pub enum AuthError {
    MissingToken,
    InvalidToken,
    InsufficientPermissions,
    ExpiredToken,
}

impl std::fmt::Display for AuthError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            AuthError::MissingToken => write!(f, "Authentication token is required"),
            AuthError::InvalidToken => write!(f, "Invalid authentication token"),
            AuthError::InsufficientPermissions => write!(f, "Insufficient permissions"),
            AuthError::ExpiredToken => write!(f, "Authentication token has expired"),
        }
    }
}

impl AuthMiddleware {
    pub fn new() -> Self {
        Self {
            api_keys: HashMap::new(),
            public_paths: vec![
                "/health".to_string(),
                "/auth/login".to_string(),
                "/auth/register".to_string(),
            ],
        }
    }

    pub fn register_api_key(&mut self, key: String, user_id: String, roles: Vec<String>) {
        self.api_keys.insert(key, AuthInfo { user_id, roles });
    }

    pub fn add_public_path(&mut self, path: String) {
        self.public_paths.push(path);
    }

    pub fn authenticate(&self, token: &str) -> Result<AuthInfo, AuthError> {
        if token.is_empty() {
            return Err(AuthError::MissingToken);
        }

        // Strip "Bearer " prefix if present
        let clean_token = token.strip_prefix("Bearer ").unwrap_or(token);

        match self.api_keys.get(clean_token) {
            Some(info) => Ok(info.clone()),
            None => Err(AuthError::InvalidToken),
        }
    }

    pub fn authorize(&self, auth_info: &AuthInfo, required_role: &str) -> Result<(), AuthError> {
        if auth_info.roles.contains(&required_role.to_string()) || auth_info.roles.contains(&"admin".to_string()) {
            Ok(())
        } else {
            Err(AuthError::InsufficientPermissions)
        }
    }

    pub fn is_public_path(&self, path: &str) -> bool {
        self.public_paths.iter().any(|p| path.starts_with(p))
    }

    pub fn validate_request(&self, path: &str, token: Option<&str>) -> Result<Option<AuthInfo>, AuthError> {
        if self.is_public_path(path) {
            return Ok(None);
        }

        match token {
            Some(t) => {
                let info = self.authenticate(t)?;
                Ok(Some(info))
            }
            None => Err(AuthError::MissingToken),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn setup_auth() -> AuthMiddleware {
        let mut auth = AuthMiddleware::new();
        auth.register_api_key(
            "valid-token-123".to_string(),
            "user-1".to_string(),
            vec!["user".to_string()],
        );
        auth.register_api_key(
            "admin-token-456".to_string(),
            "admin-1".to_string(),
            vec!["admin".to_string(), "user".to_string()],
        );
        auth
    }

    #[test]
    fn test_authenticate_valid_token() {
        let auth = setup_auth();
        let result = auth.authenticate("valid-token-123");
        assert!(result.is_ok());
        assert_eq!(result.unwrap().user_id, "user-1");
    }

    #[test]
    fn test_authenticate_bearer_prefix() {
        let auth = setup_auth();
        let result = auth.authenticate("Bearer valid-token-123");
        assert!(result.is_ok());
    }

    #[test]
    fn test_authenticate_invalid_token() {
        let auth = setup_auth();
        let result = auth.authenticate("invalid-token");
        assert!(result.is_err());
    }

    #[test]
    fn test_authenticate_empty_token() {
        let auth = setup_auth();
        let result = auth.authenticate("");
        assert!(result.is_err());
    }

    #[test]
    fn test_authorize_correct_role() {
        let auth = setup_auth();
        let info = auth.authenticate("valid-token-123").unwrap();
        assert!(auth.authorize(&info, "user").is_ok());
    }

    #[test]
    fn test_authorize_admin_has_all_access() {
        let auth = setup_auth();
        let info = auth.authenticate("admin-token-456").unwrap();
        assert!(auth.authorize(&info, "user").is_ok());
        assert!(auth.authorize(&info, "admin").is_ok());
        assert!(auth.authorize(&info, "anything").is_ok());
    }

    #[test]
    fn test_authorize_insufficient_permissions() {
        let auth = setup_auth();
        let info = auth.authenticate("valid-token-123").unwrap();
        assert!(auth.authorize(&info, "admin").is_err());
    }

    #[test]
    fn test_public_paths() {
        let auth = setup_auth();
        assert!(auth.is_public_path("/health"));
        assert!(auth.is_public_path("/auth/login"));
        assert!(!auth.is_public_path("/orders"));
    }

    #[test]
    fn test_validate_public_request() {
        let auth = setup_auth();
        let result = auth.validate_request("/health", None);
        assert!(result.is_ok());
        assert!(result.unwrap().is_none());
    }

    #[test]
    fn test_validate_protected_request_no_token() {
        let auth = setup_auth();
        let result = auth.validate_request("/orders", None);
        assert!(result.is_err());
    }

    #[test]
    fn test_validate_protected_request_with_token() {
        let auth = setup_auth();
        let result = auth.validate_request("/orders", Some("valid-token-123"));
        assert!(result.is_ok());
        assert!(result.unwrap().is_some());
    }
}

