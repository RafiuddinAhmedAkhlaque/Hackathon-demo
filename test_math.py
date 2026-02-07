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

def test_math_with_decimals(client):
    """Test operations with decimal numbers"""
    response = client.post('/math',
                          json={"operation": "add", "a": 10.5, "b": 3.2})
    assert response.status_code == 200
    data = response.get_json()
    assert data["operation"] == "add"
    assert data["a"] == 10.5
    assert data["b"] == 3.2
    assert abs(data["result"] - 13.7) < 0.0001  # Use small tolerance for float comparison

def test_math_divide_by_zero(client):
    """Test division by zero returns 400 error"""
    response = client.post('/math',
                          json={"operation": "divide", "a": 10, "b": 0})
    assert response.status_code == 400
    data = response.get_json()
    assert "Cannot divide by zero" in data["error"]

def test_math_invalid_operation(client):
    """Test invalid operation returns 400 error"""
    response = client.post('/math',
                          json={"operation": "modulo", "a": 10, "b": 3})
    assert response.status_code == 400
    data = response.get_json()
    assert "Unsupported operation" in data["error"]

def test_math_missing_operation(client):
    """Test missing operation field returns 400 error"""
    response = client.post('/math',
                          json={"a": 10, "b": 5})
    assert response.status_code == 400
    data = response.get_json()
    assert "Missing required field: operation" in data["error"]

def test_math_missing_a_field(client):
    """Test missing 'a' field returns 400 error"""
    response = client.post('/math',
                          json={"operation": "add", "b": 5})
    assert response.status_code == 400
    data = response.get_json()
    assert "Missing required field: a" in data["error"]

def test_math_missing_b_field(client):
    """Test missing 'b' field returns 400 error"""
    response = client.post('/math',
                          json={"operation": "add", "a": 10})
    assert response.status_code == 400
    data = response.get_json()
    assert "Missing required field: b" in data["error"]

def test_math_non_numeric_a(client):
    """Test non-numeric 'a' field returns 400 error"""
    response = client.post('/math',
                          json={"operation": "add", "a": "not_a_number", "b": 5})
    assert response.status_code == 400
    data = response.get_json()
    assert "must be numbers" in data["error"]

def test_math_non_numeric_b(client):
    """Test non-numeric 'b' field returns 400 error"""
    response = client.post('/math',
                          json={"operation": "add", "a": 10, "b": "not_a_number"})
    assert response.status_code == 400
    data = response.get_json()
    assert "must be numbers" in data["error"]

def test_math_empty_json(client):
    """Test empty JSON body returns 400 error"""
    response = client.post('/math', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert "Missing required field: operation" in data["error"]

def test_math_no_json_body(client):
    """Test request without JSON body returns 400 error"""
    response = client.post('/math')
    assert response.status_code == 400
    data = response.get_json()
    assert "Request body must be JSON" in data["error"]

def test_math_string_numbers_conversion(client):
    """Test that string numbers are converted to floats"""
    response = client.post('/math',
                          json={"operation": "add", "a": "10", "b": "5"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["a"] == 10.0
    assert data["b"] == 5.0
    assert data["result"] == 15.0

def test_math_negative_numbers(client):
    """Test operations with negative numbers"""
    response = client.post('/math',
                          json={"operation": "subtract", "a": -10, "b": -5})
    assert response.status_code == 200
    data = response.get_json()
    assert data["result"] == -5

def test_math_large_numbers(client):
    """Test operations with large numbers"""
    response = client.post('/math',
                          json={"operation": "multiply", "a": 1000000, "b": 1000000})
    assert response.status_code == 200
    data = response.get_json()
    assert data["result"] == 1000000000000

def test_math_precision_division(client):
    """Test division precision"""
    response = client.post('/math',
                          json={"operation": "divide", "a": 1, "b": 3})
    assert response.status_code == 200
    data = response.get_json()
    # Check that result is approximately 0.333...
    assert abs(data["result"] - (1/3)) < 0.0001