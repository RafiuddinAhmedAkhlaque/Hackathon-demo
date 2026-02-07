use std::time::Instant;
use chrono::Utc;

#[derive(Debug, Clone)]
pub struct RequestLog {
    pub request_id: String,
    pub method: String,
    pub path: String,
    pub client_ip: String,
    pub status_code: u16,
    pub duration_ms: u128,
    pub user_id: Option<String>,
    pub timestamp: String,
}

pub struct RequestLogger {
    logs: Vec<RequestLog>,
    max_logs: usize,
}

impl RequestLogger {
    pub fn new(max_logs: usize) -> Self {
        Self {
            logs: Vec::new(),
            max_logs,
        }
    }

    pub fn log_request(
        &mut self,
        request_id: &str,
        method: &str,
        path: &str,
        client_ip: &str,
        status_code: u16,
        duration_ms: u128,
        user_id: Option<String>,
    ) {
        let log = RequestLog {
            request_id: request_id.to_string(),
            method: method.to_string(),
            path: path.to_string(),
            client_ip: client_ip.to_string(),
            status_code,
            duration_ms,
            user_id,
            timestamp: Utc::now().to_rfc3339(),
        };

        self.logs.push(log);

        // Trim if over max
        if self.logs.len() > self.max_logs {
            self.logs.drain(0..self.logs.len() - self.max_logs);
        }
    }

    pub fn get_logs(&self) -> &[RequestLog] {
        &self.logs
    }

    pub fn get_logs_by_path(&self, path: &str) -> Vec<&RequestLog> {
        self.logs.iter().filter(|l| l.path.starts_with(path)).collect()
    }

    pub fn get_logs_by_status(&self, status: u16) -> Vec<&RequestLog> {
        self.logs.iter().filter(|l| l.status_code == status).collect()
    }

    pub fn get_error_rate(&self) -> f64 {
        if self.logs.is_empty() {
            return 0.0;
        }
        let errors = self.logs.iter().filter(|l| l.status_code >= 400).count();
        (errors as f64 / self.logs.len() as f64) * 100.0
    }

    pub fn get_average_duration(&self) -> f64 {
        if self.logs.is_empty() {
            return 0.0;
        }
        let total: u128 = self.logs.iter().map(|l| l.duration_ms).sum();
        total as f64 / self.logs.len() as f64
    }

    pub fn count(&self) -> usize {
        self.logs.len()
    }

    pub fn clear(&mut self) {
        self.logs.clear();
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn create_logger_with_data() -> RequestLogger {
        let mut logger = RequestLogger::new(1000);
        logger.log_request("req-1", "GET", "/users", "127.0.0.1", 200, 50, Some("user-1".to_string()));
        logger.log_request("req-2", "POST", "/orders", "127.0.0.1", 201, 120, Some("user-1".to_string()));
        logger.log_request("req-3", "GET", "/products", "192.168.1.1", 404, 10, None);
        logger.log_request("req-4", "GET", "/users/123", "127.0.0.1", 500, 200, None);
        logger
    }

    #[test]
    fn test_log_request() {
        let mut logger = RequestLogger::new(100);
        logger.log_request("req-1", "GET", "/test", "127.0.0.1", 200, 50, None);
        assert_eq!(logger.count(), 1);
    }

    #[test]
    fn test_max_logs_trimming() {
        let mut logger = RequestLogger::new(2);
        logger.log_request("req-1", "GET", "/a", "127.0.0.1", 200, 10, None);
        logger.log_request("req-2", "GET", "/b", "127.0.0.1", 200, 10, None);
        logger.log_request("req-3", "GET", "/c", "127.0.0.1", 200, 10, None);
        assert_eq!(logger.count(), 2);
    }

    #[test]
    fn test_get_logs_by_path() {
        let logger = create_logger_with_data();
        let user_logs = logger.get_logs_by_path("/users");
        assert_eq!(user_logs.len(), 2); // /users and /users/123
    }

    #[test]
    fn test_get_logs_by_status() {
        let logger = create_logger_with_data();
        let not_found = logger.get_logs_by_status(404);
        assert_eq!(not_found.len(), 1);
    }

    #[test]
    fn test_error_rate() {
        let logger = create_logger_with_data();
        let rate = logger.get_error_rate();
        // 2 errors out of 4 requests = 50%
        assert!((rate - 50.0).abs() < 0.1);
    }

    #[test]
    fn test_average_duration() {
        let logger = create_logger_with_data();
        let avg = logger.get_average_duration();
        // (50 + 120 + 10 + 200) / 4 = 95.0
        assert!((avg - 95.0).abs() < 0.1);
    }

    #[test]
    fn test_clear_logs() {
        let mut logger = create_logger_with_data();
        logger.clear();
        assert_eq!(logger.count(), 0);
    }

    #[test]
    fn test_empty_logger_error_rate() {
        let logger = RequestLogger::new(100);
        assert_eq!(logger.get_error_rate(), 0.0);
    }

    #[test]
    fn test_empty_logger_avg_duration() {
        let logger = RequestLogger::new(100);
        assert_eq!(logger.get_average_duration(), 0.0);
    }
}

