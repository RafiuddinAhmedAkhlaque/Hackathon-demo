"""
Unit tests for the math endpoint
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
    response = client.post('/math', 
                          json={"operation": "add", "a": 10, "b": 5})
    assert response.status_code == 200
    data = response.get_json()
    assert data["operation"] == "add"
    assert data["a"] == 10
    assert data["b"] == 5
    assert data["result"] == 15

def test_math_subtract_operation(client):
    """Test subtraction operation"""
    response = client.post('/math', 
                          json={"operation": "subtract", "a": 10, "b": 3})
    assert response.status_code == 200
    data = response.get_json()
    assert data["operation"] == "subtract"
    assert data["a"] == 10
    assert data["b"] == 3
    assert data["result"] == 7

def test_math_multiply_operation(client):
    """Test multiplication operation"""
    response = client.post('/math', 
                          json={"operation": "multiply", "a": 4, "b": 6})
    assert response.status_code == 200
    data = response.get_json()
    assert data["operation"] == "multiply"
    assert data["a"] == 4
    assert data["b"] == 6
    assert data["result"] == 24

def test_math_divide_operation(client):
    """Test division operation"""
    response = client.post('/math', 
                          json={"operation": "divide", "a": 20, "b": 4})
    assert response.status_code == 200
    data = response.get_json()
    assert data["operation"] == "divide"
    assert data["a"] == 20
    assert data["b"] == 4
    assert data["result"] == 5

# Test decimal/float support

def test_math_add_decimals(client):
    """Test addition with decimal numbers"""
    response = client.post('/math', 
                          json={"operation": "add", "a": 10.5, "b": 5.25})
    assert response.status_code == 200
    data = response.get_json()
    assert data["result"] == 15.75

def test_math_divide_decimals(client):
    """Test division with decimal result"""
    response = client.post('/math', 
                          json={"operation": "divide", "a": 10, "b": 3})
    assert response.status_code == 200
    data = response.get_json()
    assert abs(data["result"] - 3.3333333333333335) < 0.0001  # Handle floating point precision

def test_math_negative_numbers(client):
    """Test operations with negative numbers"""
    response = client.post('/math', 
                          json={"operation": "subtract", "a": 5, "b": -3})
    assert response.status_code == 200
    data = response.get_json()
    assert data["result"] == 8

# Test error cases

def test_math_missing_operation(client):
    """Test missing operation field"""
    response = client.post('/math', 
                          json={"a": 10, "b": 5})
    assert response.status_code == 400
    data = response.get_json()
    assert "Missing required field: operation" in data["error"]

def test_math_missing_a(client):
    """Test missing 'a' field"""
    response = client.post('/math', 
                          json={"operation": "add", "b": 5})
    assert response.status_code == 400
    data = response.get_json()
    assert "Missing required field: a" in data["error"]

def test_math_missing_b(client):
    """Test missing 'b' field"""
    response = client.post('/math', 
                          json={"operation": "add", "a": 10})
    assert response.status_code == 400
    data = response.get_json()
    assert "Missing required field: b" in data["error"]

def test_math_unsupported_operation(client):
    """Test unsupported operation"""
    response = client.post('/math', 
                          json={"operation": "power", "a": 10, "b": 2})
    assert response.status_code == 400
    data = response.get_json()
    assert "Unsupported operation" in data["error"]

def test_math_divide_by_zero(client):
    """Test division by zero error"""
    response = client.post('/math', 
                          json={"operation": "divide", "a": 10, "b": 0})
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Cannot divide by zero"

def test_math_invalid_number_a(client):
    """Test invalid number for 'a'"""
    response = client.post('/math', 
                          json={"operation": "add", "a": "not_a_number", "b": 5})
    assert response.status_code == 400
    data = response.get_json()
    assert "Values a and b must be numbers" in data["error"]

def test_math_invalid_number_b(client):
    """Test invalid number for 'b'"""
    response = client.post('/math', 
                          json={"operation": "add", "a": 10, "b": "not_a_number"})
    assert response.status_code == 400
    data = response.get_json()
    assert "Values a and b must be numbers" in data["error"]

def test_math_no_json_data(client):
    """Test request without JSON data"""
    response = client.post('/math')
    assert response.status_code == 400
    data = response.get_json()
    assert "No JSON data provided" in data["error"]

def test_math_empty_json(client):
    """Test request with empty JSON"""
    response = client.post('/math', json={})
    assert response.status_code == 400

# Test edge cases

def test_math_zero_values(client):
    """Test operations with zero values"""
    response = client.post('/math', 
                          json={"operation": "multiply", "a": 0, "b": 100})
    assert response.status_code == 200
    data = response.get_json()
    assert data["result"] == 0

def test_math_large_numbers(client):
    """Test operations with large numbers"""
    response = client.post('/math', 
                          json={"operation": "add", "a": 1000000, "b": 2000000})
    assert response.status_code == 200
    data = response.get_json()
    assert data["result"] == 3000000

def test_math_string_numbers(client):
    """Test that string representations of numbers work"""
    response = client.post('/math', 
                          json={"operation": "add", "a": "10.5", "b": "5.5"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["result"] == 16.0