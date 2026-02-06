"""
Unit tests for the hello endpoint
"""
import pytest
from datetime import datetime
from app import app

@pytest.fixture
def client():
    """Create a test client for the Flask application"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_hello_endpoint_returns_200(client):
    """Test that GET /hello returns 200 status code"""
    response = client.get('/hello')
    assert response.status_code == 200

def test_hello_endpoint_contains_hello_world(client):
    """Test that response contains 'Hello, World!'"""
    response = client.get('/hello')
    data = response.get_json()
    assert "Hello, World!" in data["message"]

def test_hello_endpoint_response_format(client):
    """Test that the response is in correct JSON format"""
    response = client.get('/hello')
    data = response.get_json()
    assert isinstance(data, dict)
    assert "message" in data
    assert data["message"] == "Hello, World!"

def test_goodbye_endpoint_returns_200(client):
    """Test that GET /goodbye returns 200 status code"""
    response = client.get('/goodbye')
    assert response.status_code == 200

def test_goodbye_endpoint_contains_goodbye_world(client):
    """Test that response contains 'Goodbye, World!'"""
    response = client.get('/goodbye')
    data = response.get_json()
    assert "Goodbye, World!" in data["message"]

def test_goodbye_endpoint_response_format(client):
    """Test that the response is in correct JSON format"""
    response = client.get('/goodbye')
    data = response.get_json()
    assert isinstance(data, dict)
    assert "message" in data
    assert data["message"] == "Goodbye, World!"

def test_health_endpoint_returns_200(client):
    """Test that GET /health returns 200 status code"""
    response = client.get('/health')
    assert response.status_code == 200

def test_health_endpoint_response_format(client):
    """Test that the health response is in correct JSON format"""
    response = client.get('/health')
    data = response.get_json()
    assert isinstance(data, dict)
    assert "status" in data
    assert "timestamp" in data
    assert "version" in data

def test_health_endpoint_status_healthy(client):
    """Test that health endpoint returns status 'healthy'"""
    response = client.get('/health')
    data = response.get_json()
    assert data["status"] == "healthy"

def test_health_endpoint_version(client):
    """Test that health endpoint returns version '1.0.0'"""
    response = client.get('/health')
    data = response.get_json()
    assert data["version"] == "1.0.0"

def test_health_endpoint_timestamp_format(client):
    """Test that health endpoint returns a valid ISO format timestamp"""
    response = client.get('/health')
    data = response.get_json()
    timestamp = data["timestamp"]
    
    # Verify timestamp is a string and ends with 'Z' (UTC indicator)
    assert isinstance(timestamp, str)
    assert timestamp.endswith('Z')
    
    # Verify we can parse the timestamp (will raise exception if invalid)
    parsed_timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    assert isinstance(parsed_timestamp, datetime)