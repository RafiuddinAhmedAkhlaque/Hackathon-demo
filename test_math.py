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
        "b": 7
    }
    response = client.post('/math', json=data)
    assert response.status_code == 200
    result = response.get_json()
    assert result["operation"] == "multiply"
    assert result["a"] == 4
    assert result["b"] == 7
    assert result["result"] == 28

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

def test_math_divide_by_zero(client):
    """Test division by zero returns 400 with proper message"""
    data = {
        "operation": "divide",
        "a": 10,
        "b": 0
    }
    response = client.post('/math', json=data)
    assert response.status_code == 400
    result = response.get_json()
    assert result["error"] == "Cannot divide by zero"

def test_math_with_decimals(client):
    """Test operations with decimal numbers"""
    data = {
        "operation": "add",
        "a": 10.5,
        "b": 5.25
    }
    response = client.post('/math', json=data)
    assert response.status_code == 200
    result = response.get_json()
    assert result["operation"] == "add"
    assert result["a"] == 10.5
    assert result["b"] == 5.25
    assert result["result"] == 15.75

def test_math_with_negative_numbers(client):
    """Test operations with negative numbers"""
    data = {
        "operation": "subtract",
        "a": -5,
        "b": 3
    }
    response = client.post('/math', json=data)
    assert response.status_code == 200
    result = response.get_json()
    assert result["operation"] == "subtract"
    assert result["a"] == -5
    assert result["b"] == 3
    assert result["result"] == -8

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
    assert "Unsupported operation" in result["error"]

def test_math_missing_operation_field(client):
    """Test missing operation field returns 400"""
    data = {
        "a": 10,
        "b": 5
    }
    response = client.post('/math', json=data)
    assert response.status_code == 400
    result = response.get_json()
    assert result["error"] == "Missing required field: operation"

def test_math_missing_a_field(client):
    """Test missing 'a' field returns 400"""
    data = {
        "operation": "add",
        "b": 5
    }
    response = client.post('/math', json=data)
    assert response.status_code == 400
    result = response.get_json()
    assert result["error"] == "Missing required field: a"

def test_math_missing_b_field(client):
    """Test missing 'b' field returns 400"""
    data = {
        "operation": "add",
        "a": 10
    }
    response = client.post('/math', json=data)
    assert response.status_code == 400
    result = response.get_json()
    assert result["error"] == "Missing required field: b"

def test_math_invalid_number_for_a(client):
    """Test invalid number for 'a' returns 400"""
    data = {
        "operation": "add",
        "a": "not_a_number",
        "b": 5
    }
    response = client.post('/math', json=data)
    assert response.status_code == 400
    result = response.get_json()
    assert "must be valid numbers" in result["error"]

def test_math_invalid_number_for_b(client):
    """Test invalid number for 'b' returns 400"""
    data = {
        "operation": "add",
        "a": 10,
        "b": "not_a_number"
    }
    response = client.post('/math', json=data)
    assert response.status_code == 400
    result = response.get_json()
    assert "must be valid numbers" in result["error"]

def test_math_non_json_request(client):
    """Test non-JSON request returns 400"""
    response = client.post('/math', data="not json", content_type='text/plain')
    assert response.status_code == 400
    result = response.get_json()
    assert result["error"] == "Content-Type must be application/json"

def test_math_empty_request_body(client):
    """Test empty JSON request body"""
    response = client.post('/math', json={})
    assert response.status_code == 400
    result = response.get_json()
    assert result["error"] == "Missing required field: operation"

def test_math_precision_with_division(client):
    """Test division precision with decimal results"""
    data = {
        "operation": "divide",
        "a": 10,
        "b": 3
    }
    response = client.post('/math', json=data)
    assert response.status_code == 200
    result = response.get_json()
    assert result["operation"] == "divide"
    assert result["a"] == 10
    assert result["b"] == 3
    assert abs(result["result"] - 3.3333333333333335) < 1e-10  # Handle floating point precision

def test_math_large_numbers(client):
    """Test operations with large numbers"""
    data = {
        "operation": "multiply",
        "a": 1000000,
        "b": 2000000
    }
    response = client.post('/math', json=data)
    assert response.status_code == 200
    result = response.get_json()
    assert result["operation"] == "multiply"
    assert result["a"] == 1000000
    assert result["b"] == 2000000
    assert result["result"] == 2000000000000