"""Tests for request logging middleware."""
import json
import pytest
from unittest.mock import patch
from app import create_app


@pytest.fixture
def app():
    """Create test application."""
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


class TestRequestLogging:
    """Test cases for request logging middleware."""
    
    @patch('app.logger')
    def test_health_endpoint_logging(self, mock_logger, client):
        """Test that health endpoint requests are logged in JSON format."""
        response = client.get('/health')
        
        assert response.status_code == 200
        assert mock_logger.info.called
        
        # Get the logged message
        logged_call = mock_logger.info.call_args[0][0]
        log_data = json.loads(logged_call)
        
        # Validate JSON structure
        assert 'method' in log_data
        assert 'path' in log_data
        assert 'status' in log_data
        assert 'duration_ms' in log_data
        assert 'timestamp' in log_data
        
        # Validate specific values
        assert log_data['method'] == 'GET'
        assert log_data['path'] == '/health'
        assert log_data['status'] == 200
        assert isinstance(log_data['duration_ms'], (int, float))
        assert log_data['duration_ms'] >= 0
        assert log_data['timestamp'].endswith('Z')  # UTC timestamp
    
    @patch('app.logger')
    def test_hello_endpoint_logging(self, mock_logger, client):
        """Test that hello endpoint requests are logged in JSON format."""
        response = client.get('/hello')
        
        assert response.status_code == 200
        assert mock_logger.info.called
        
        # Get the logged message
        logged_call = mock_logger.info.call_args[0][0]
        log_data = json.loads(logged_call)
        
        # Validate JSON structure
        assert 'method' in log_data
        assert 'path' in log_data
        assert 'status' in log_data
        assert 'duration_ms' in log_data
        assert 'timestamp' in log_data
        
        # Validate specific values
        assert log_data['method'] == 'GET'
        assert log_data['path'] == '/hello'
        assert log_data['status'] == 200
        assert isinstance(log_data['duration_ms'], (int, float))
        assert log_data['duration_ms'] >= 0
    
    @patch('app.logger')
    def test_stock_endpoint_logging(self, mock_logger, client):
        """Test that stock endpoint requests are logged in JSON format."""
        response = client.get('/stock/')
        
        assert response.status_code == 200
        assert mock_logger.info.called
        
        # Get the logged message
        logged_call = mock_logger.info.call_args[0][0]
        log_data = json.loads(logged_call)
        
        # Validate JSON structure and values
        assert log_data['method'] == 'GET'
        assert log_data['path'] == '/stock/'
        assert log_data['status'] == 200
        assert isinstance(log_data['duration_ms'], (int, float))
        assert 'timestamp' in log_data
    
    @patch('app.logger')
    def test_stock_item_endpoint_logging(self, mock_logger, client):
        """Test that stock item endpoint requests are logged in JSON format."""
        response = client.get('/stock/12345')
        
        assert response.status_code == 200
        assert mock_logger.info.called
        
        # Get the logged message
        logged_call = mock_logger.info.call_args[0][0]
        log_data = json.loads(logged_call)
        
        # Validate JSON structure and values
        assert log_data['method'] == 'GET'
        assert log_data['path'] == '/stock/12345'
        assert log_data['status'] == 200
        assert isinstance(log_data['duration_ms'], (int, float))
        assert 'timestamp' in log_data
    
    @patch('app.logger')
    def test_404_endpoint_logging(self, mock_logger, client):
        """Test that 404 responses are logged correctly."""
        response = client.get('/nonexistent')
        
        assert response.status_code == 404
        assert mock_logger.info.called
        
        # Get the logged message
        logged_call = mock_logger.info.call_args[0][0]
        log_data = json.loads(logged_call)
        
        # Validate JSON structure and values
        assert log_data['method'] == 'GET'
        assert log_data['path'] == '/nonexistent'
        assert log_data['status'] == 404
        assert isinstance(log_data['duration_ms'], (int, float))
        assert 'timestamp' in log_data
    
    @patch('app.logger')
    def test_warehouse_endpoint_logging(self, mock_logger, client):
        """Test that warehouse endpoint requests are logged in JSON format."""
        response = client.get('/warehouses/')
        
        assert response.status_code == 200
        assert mock_logger.info.called
        
        # Get the logged message  
        logged_call = mock_logger.info.call_args[0][0]
        log_data = json.loads(logged_call)
        
        # Validate JSON structure and values
        assert log_data['method'] == 'GET'
        assert log_data['path'] == '/warehouses/'
        assert log_data['status'] == 200
        assert isinstance(log_data['duration_ms'], (int, float))
        assert 'timestamp' in log_data
    
    def test_logged_json_is_valid(self, client):
        """Test that all logged output is valid JSON."""
        with patch('app.logger') as mock_logger:
            client.get('/health')
            client.get('/stock/')
            client.get('/warehouses/')
            
            # Check that all logged messages are valid JSON
            for call in mock_logger.info.call_args_list:
                logged_message = call[0][0]
                # This should not raise an exception
                json.loads(logged_message)
    
    def test_no_old_string_format_used(self, client):
        """Test that the old string format is no longer used."""
        with patch('app.logger') as mock_logger:
            client.get('/hello')
            
            logged_call = mock_logger.info.call_args[0][0]
            
            # Ensure old format strings are not present
            assert "Request: GET /hello" not in logged_call
            assert "Status: 200" not in logged_call
            assert "Duration:" not in logged_call
            
            # Ensure it is valid JSON
            log_data = json.loads(logged_call)
            assert isinstance(log_data, dict)