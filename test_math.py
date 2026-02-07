"""
Unit tests for the /math endpoint
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

# Test successful operations
def test_math_add_operation(client):
    """Test addition operation"""
    data = {
        "operation": "add",
        "a": 10,
        "b": 5
    }
    response = client.post('/math', json=data)
    assert response.status_code == 200
    result = response.get_json()
    assert result["operation"] == "add"
    assert result["a"] == 10
    assert result["b"] == 5
    assert result["result"] == 15

def test_math_subtract_operation(client):
    """Test subtraction operation"""
    data = {
        "operation": "subtract",
        "a": 10,
        "b": 3
    }
    response = client.post('/math', json=data)
    assert response.status_code == 200
    result = response.get_json()
    assert result["operation"] == "subtract"
    assert result["a"] == 10
    assert result["b"] == 3
    assert result["result"] == 7

def test_math_multiply_operation(client):
    """Test multiplication operation"""
    data = {
        "operation": "multiply",
        "a": 4,
        "b": 6
    }
    response = client.post('/math', json=data)
    assert response.status_code == 200
    result = response.get_json()
    assert result["operation"] == "multiply"
    assert result["a"] == 4
    assert result["b"] == 6
    assert result["result"] == 24

def test_math_divide_operation(client):
    """Test division operation"""
    data = {
        "operation": "divide",
        "a": 20,
        "b": 4
    }
    response = client.post('/math', json=data)
    assert response.status_code == 200
    result = response.get_json()
    assert result["operation"] == "divide"
    assert result["a"] == 20
    assert result["b"] == 4
    assert result["result"] == 5

# Test with decimal numbers
def test_math_add_decimals(client):
    """Test addition with decimal numbers"""
    data = {
        "operation": "add",
        "a": 10.5,
        "b": 2.3
    }
    response = client.post('/math', json=data)
    assert response.status_code == 200
    result = response.get_json()
    assert result["operation"] == "add"
    assert result["a"] == 10.5
    assert result["b"] == 2.3
    assert abs(result["result"] - 12.8) < 0.0001  # Use abs for float comparison

def test_math_divide_decimals(client):
    """Test division with decimal numbers"""
    data = {
        "operation": "divide",
        "a": 7.5,
        "b": 2.5
    }
    response = client.post('/math', json=data)
    assert response.status_code == 200
    result = response.get_json()
    assert result["operation"] == "divide"
    assert result["a"] == 7.5
    assert result["b"] == 2.5
    assert result["result"] == 3.0

# Test negative numbers
def test_math_negative_numbers(client):
    """Test operations with negative numbers"""
    data = {
        "operation": "subtract",
        "a": -5,
        "b": 3
    }
    response = client.post('/math', json=data)
    assert response.status_code == 200
    result = response.get_json()
    assert result["result"] == -8

# Test error cases
def test_math_unsupported_operation(client):
    """Test unsupported operation returns 400"""
    data = {
        "operation": "power",
        "a": 2,
        "b": 3
    }
    response = client.post('/math', json=data)
    assert response.status_code == 400
    result = response.get_json()
    assert "error" in result
    assert "Unsupported operation" in result["error"]

def test_math_missing_operation(client):
    """Test missing operation field returns 400"""
    data = {
        "a": 10,
        "b": 5
    }
    response = client.post('/math', json=data)
    assert response.status_code == 400
    result = response.get_json()
    assert "error" in result
    assert "Missing required field: operation" in result["error"]

def test_math_missing_a(client):
    """Test missing 'a' field returns 400"""
    data = {
        "operation": "add",
        "b": 5
    }
    response = client.post('/math', json=data)
    assert response.status_code == 400
    result = response.get_json()
    assert "error" in result
    assert "Missing required field: a" in result["error"]

def test_math_missing_b(client):
    """Test missing 'b' field returns 400"""
    data = {
        "operation": "add",
        "a": 10
    }
    response = client.post('/math', json=data)
    assert response.status_code == 400
    result = response.get_json()
    assert "error" in result
    assert "Missing required field: b" in result["error"]

def test_math_divide_by_zero(client):
    """Test division by zero returns 400 with specific message"""
    data = {
        "operation": "divide",
        "a": 10,
        "b": 0
    }
    response = client.post('/math', json=data)
    assert response.status_code == 400
    result = response.get_json()
    assert "error" in result
    assert result["error"] == "Cannot divide by zero"

def test_math_invalid_number_a(client):
    """Test invalid number for 'a' returns 400"""
    data = {
        "operation": "add",
        "a": "not_a_number",
        "b": 5
    }
    response = client.post('/math', json=data)
    assert response.status_code == 400
    result = response.get_json()
    assert "error" in result
    assert "must be numbers" in result["error"]

def test_math_invalid_number_b(client):
    """Test invalid number for 'b' returns 400"""
    data = {
        "operation": "add",
        "a": 10,
        "b": "not_a_number"
    }
    response = client.post('/math', json=data)
    assert response.status_code == 400
    result = response.get_json()
    assert "error" in result
    assert "must be numbers" in result["error"]

def test_math_no_json_data(client):
    """Test request without JSON data returns 400"""
    response = client.post('/math', data='not json', content_type='text/plain')
    assert response.status_code == 400
    result = response.get_json()
    assert "error" in result
    assert "Request must contain valid JSON data" in result["error"]

def test_math_empty_json(client):
    """Test empty JSON data returns 400"""
    response = client.post('/math', json={})
    assert response.status_code == 400
    result = response.get_json()
    assert "error" in result
    assert "Missing required field: operation" in result["error"]

# Test string numbers (should be converted to float)
def test_math_string_numbers(client):
    """Test that string numbers are properly converted"""
    data = {
        "operation": "add",
        "a": "10",
        "b": "5"
    }
    response = client.post('/math', json=data)
    assert response.status_code == 200
    result = response.get_json()
    assert result["result"] == 15

def test_math_mixed_string_float(client):
    """Test mixed string and float numbers"""
    data = {
        "operation": "multiply",
        "a": "3.5",
        "b": 2
    }
    response = client.post('/math', json=data)
    assert response.status_code == 200
    result = response.get_json()
    assert result["result"] == 7.0