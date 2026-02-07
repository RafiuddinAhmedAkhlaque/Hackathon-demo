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
    response = client.post('/math',
                          data=json.dumps({"operation": "add", "a": 10, "b": 5}),
                          content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data["operation"] == "add"
    assert data["a"] == 10.0
    assert data["b"] == 5.0
    assert data["result"] == 15.0

def test_math_subtract_operation(client):
    """Test subtraction operation"""
    response = client.post('/math',
                          data=json.dumps({"operation": "subtract", "a": 10, "b": 5}),
                          content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data["operation"] == "subtract"
    assert data["a"] == 10.0
    assert data["b"] == 5.0
    assert data["result"] == 5.0

def test_math_multiply_operation(client):
    """Test multiplication operation"""
    response = client.post('/math',
                          data=json.dumps({"operation": "multiply", "a": 10, "b": 5}),
                          content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data["operation"] == "multiply"
    assert data["a"] == 10.0
    assert data["b"] == 5.0
    assert data["result"] == 50.0

def test_math_divide_operation(client):
    """Test division operation"""
    response = client.post('/math',
                          data=json.dumps({"operation": "divide", "a": 10, "b": 5}),
                          content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data["operation"] == "divide"
    assert data["a"] == 10.0
    assert data["b"] == 5.0
    assert data["result"] == 2.0

# Test with decimal/float numbers

def test_math_add_with_decimals(client):
    """Test addition with decimal numbers"""
    response = client.post('/math',
                          data=json.dumps({"operation": "add", "a": 10.5, "b": 5.3}),
                          content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data["result"] == pytest.approx(15.8)

def test_math_divide_with_decimals(client):
    """Test division with decimal numbers"""
    response = client.post('/math',
                          data=json.dumps({"operation": "divide", "a": 10.5, "b": 2.5}),
                          content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data["result"] == pytest.approx(4.2)

# Test error cases

def test_math_unsupported_operation(client):
    """Test unsupported operation returns 400"""
    response = client.post('/math',
                          data=json.dumps({"operation": "power", "a": 10, "b": 5}),
                          content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "Unsupported operation" in data["error"]

def test_math_missing_operation_field(client):
    """Test missing operation field returns 400"""
    response = client.post('/math',
                          data=json.dumps({"a": 10, "b": 5}),
                          content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "Missing required field: operation" in data["error"]

def test_math_missing_a_field(client):
    """Test missing 'a' field returns 400"""
    response = client.post('/math',
                          data=json.dumps({"operation": "add", "b": 5}),
                          content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "Missing required field: a" in data["error"]

def test_math_missing_b_field(client):
    """Test missing 'b' field returns 400"""
    response = client.post('/math',
                          data=json.dumps({"operation": "add", "a": 10}),
                          content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "Missing required field: b" in data["error"]

def test_math_divide_by_zero(client):
    """Test division by zero returns 400 with specific message"""
    response = client.post('/math',
                          data=json.dumps({"operation": "divide", "a": 10, "b": 0}),
                          content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Cannot divide by zero"

def test_math_invalid_number_a(client):
    """Test invalid number for 'a' returns 400"""
    response = client.post('/math',
                          data=json.dumps({"operation": "add", "a": "not_a_number", "b": 5}),
                          content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "must be valid numbers" in data["error"]

def test_math_invalid_number_b(client):
    """Test invalid number for 'b' returns 400"""
    response = client.post('/math',
                          data=json.dumps({"operation": "add", "a": 10, "b": "not_a_number"}),
                          content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "must be valid numbers" in data["error"]

def test_math_non_json_request(client):
    """Test non-JSON request returns 400"""
    response = client.post('/math',
                          data="operation=add&a=10&b=5",
                          content_type='application/x-www-form-urlencoded')
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "Request must be JSON" in data["error"]

# Test edge cases

def test_math_negative_numbers(client):
    """Test operations with negative numbers"""
    response = client.post('/math',
                          data=json.dumps({"operation": "add", "a": -10, "b": 5}),
                          content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data["result"] == -5.0

def test_math_zero_operands(client):
    """Test operations with zero operands"""
    response = client.post('/math',
                          data=json.dumps({"operation": "multiply", "a": 0, "b": 5}),
                          content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data["result"] == 0.0

def test_math_large_numbers(client):
    """Test operations with large numbers"""
    response = client.post('/math',
                          data=json.dumps({"operation": "add", "a": 1000000, "b": 2000000}),
                          content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data["result"] == 3000000.0