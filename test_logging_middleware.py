"""
Unit tests for the logging middleware
"""
import logging
import pytest
from app import app

@pytest.fixture
def client():
    """Create a test client for the Flask application"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_logging_middleware_logs_request_info(client, caplog):
    """Test that the logging middleware logs request information"""
    with caplog.at_level(logging.INFO):
        response = client.get('/hello')
        
        # Verify the response is successful
        assert response.status_code == 200
        
        # Verify that a log entry was created
        assert len(caplog.records) > 0
        
        # Check the log message content
        log_message = caplog.records[0].message
        assert "Request: GET /hello" in log_message
        assert "Status: 200" in log_message
        assert "Duration:" in log_message
        assert "ms" in log_message

def test_logging_middleware_logs_different_endpoints(client, caplog):
    """Test that the logging middleware works for different endpoints"""
    with caplog.at_level(logging.INFO):
        # Test /hello endpoint
        response1 = client.get('/hello')
        assert response1.status_code == 200
        
        # Test /goodbye endpoint
        response2 = client.get('/goodbye')
        assert response2.status_code == 200
        
        # Verify both requests were logged
        assert len(caplog.records) >= 2
        
        # Check that both endpoints are logged
        log_messages = [record.message for record in caplog.records]
        hello_logged = any("GET /hello" in msg for msg in log_messages)
        goodbye_logged = any("GET /goodbye" in msg for msg in log_messages)
        
        assert hello_logged, "Hello endpoint should be logged"
        assert goodbye_logged, "Goodbye endpoint should be logged"

def test_logging_middleware_logs_404_responses(client, caplog):
    """Test that the logging middleware logs 404 responses"""
    with caplog.at_level(logging.INFO):
        response = client.get('/nonexistent')
        
        # Verify the response is 404
        assert response.status_code == 404
        
        # Verify that a log entry was created
        assert len(caplog.records) > 0
        
        # Check the log message content
        log_message = caplog.records[0].message
        assert "Request: GET /nonexistent" in log_message
        assert "Status: 404" in log_message
        assert "Duration:" in log_message
        assert "ms" in log_message