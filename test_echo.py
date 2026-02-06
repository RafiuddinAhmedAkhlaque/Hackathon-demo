"""
Unit tests for the echo endpoint
"""
import pytest
import json
from app import app

@pytest.fixture
def client():
    """Create a test client for the Flask application"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_echo_endpoint_valid_message(client):
    """Test that POST /echo returns correct response for valid message"""
    response = client.post('/echo', 
                          data=json.dumps({"message": "Hello world"}),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = response.get_json()
    
    assert data["original_message"] == "Hello world"
    assert data["character_count"] == 11
    assert data["word_count"] == 2
    assert data["reversed"] == "dlrow olleH"
    assert data["uppercase"] == "HELLO WORLD"
    assert "timestamp" in data
    assert data["timestamp"].endswith("Z")  # ISO format with Z

def test_echo_endpoint_empty_string(client):
    """Test that POST /echo handles empty strings gracefully"""
    response = client.post('/echo', 
                          data=json.dumps({"message": ""}),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = response.get_json()
    
    assert data["original_message"] == ""
    assert data["character_count"] == 0
    assert data["word_count"] == 0
    assert data["reversed"] == ""
    assert data["uppercase"] == ""
    assert "timestamp" in data

def test_echo_endpoint_single_word(client):
    """Test that POST /echo works with single word"""
    response = client.post('/echo', 
                          data=json.dumps({"message": "test"}),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = response.get_json()
    
    assert data["original_message"] == "test"
    assert data["character_count"] == 4
    assert data["word_count"] == 1
    assert data["reversed"] == "tset"
    assert data["uppercase"] == "TEST"

def test_echo_endpoint_whitespace_only(client):
    """Test that POST /echo handles whitespace-only strings"""
    response = client.post('/echo', 
                          data=json.dumps({"message": "   "}),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = response.get_json()
    
    assert data["original_message"] == "   "
    assert data["character_count"] == 3
    assert data["word_count"] == 0  # No actual words, just whitespace
    assert data["reversed"] == "   "
    assert data["uppercase"] == "   "

def test_echo_endpoint_missing_message_field(client):
    """Test that POST /echo returns 400 when message field is missing"""
    response = client.post('/echo', 
                          data=json.dumps({"other_field": "value"}),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "message" in data["error"].lower()

def test_echo_endpoint_no_json_body(client):
    """Test that POST /echo returns 400 when no JSON body is provided"""
    response = client.post('/echo', 
                          data=json.dumps({}),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

def test_echo_endpoint_invalid_content_type(client):
    """Test that POST /echo returns 400 for non-JSON content type"""
    response = client.post('/echo', 
                          data="message=test",
                          content_type='application/x-www-form-urlencoded')
    
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

def test_echo_endpoint_invalid_json(client):
    """Test that POST /echo returns 400 for invalid JSON"""
    response = client.post('/echo', 
                          data="{invalid json}",
                          content_type='application/json')
    
    assert response.status_code == 400

def test_echo_endpoint_non_string_message(client):
    """Test that POST /echo returns 400 when message is not a string"""
    response = client.post('/echo', 
                          data=json.dumps({"message": 123}),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "string" in data["error"].lower()

def test_echo_endpoint_complex_message(client):
    """Test that POST /echo handles complex messages with special characters"""
    complex_message = "Hello, World! 123 @#$%"
    response = client.post('/echo', 
                          data=json.dumps({"message": complex_message}),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = response.get_json()
    
    assert data["original_message"] == complex_message
    assert data["character_count"] == len(complex_message)
    assert data["word_count"] == 4  # "Hello,", "World!", "123", "@#$%"
    assert data["reversed"] == complex_message[::-1]
    assert data["uppercase"] == complex_message.upper()

def test_echo_endpoint_multiple_spaces(client):
    """Test that POST /echo handles messages with multiple spaces correctly"""
    message_with_spaces = "Hello    world   test"
    response = client.post('/echo', 
                          data=json.dumps({"message": message_with_spaces}),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = response.get_json()
    
    assert data["original_message"] == message_with_spaces
    assert data["character_count"] == len(message_with_spaces)
    assert data["word_count"] == 3  # "Hello", "world", "test" (split handles multiple spaces)
    assert data["reversed"] == message_with_spaces[::-1]
    assert data["uppercase"] == message_with_spaces.upper()