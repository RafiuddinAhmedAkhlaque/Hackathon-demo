"""
Unit tests for the hello endpoint
"""
import pytest
import re
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
    assert "timestamp" in data
    assert data["message"] == "Hello, World!"

def test_hello_endpoint_timestamp_format(client):
    """Test that the timestamp is in ISO 8601 format"""
    response = client.get('/hello')
    data = response.get_json()
    timestamp = data["timestamp"]
    # Check ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ
    iso_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$'
    assert re.match(iso_pattern, timestamp), f"Timestamp '{timestamp}' is not in ISO 8601 format"

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
    assert "timestamp" in data
    assert data["message"] == "Goodbye, World!"

def test_goodbye_endpoint_timestamp_format(client):
    """Test that the timestamp is in ISO 8601 format"""
    response = client.get('/goodbye')
    data = response.get_json()
    timestamp = data["timestamp"]
    # Check ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ
    iso_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$'
    assert re.match(iso_pattern, timestamp), f"Timestamp '{timestamp}' is not in ISO 8601 format"

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
    assert data["status"] == "healthy"

def test_health_endpoint_timestamp_format(client):
    """Test that the health timestamp is in ISO 8601 format"""
    response = client.get('/health')
    data = response.get_json()
    timestamp = data["timestamp"]
    # Check ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ
    iso_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$'
    assert re.match(iso_pattern, timestamp), f"Timestamp '{timestamp}' is not in ISO 8601 format"