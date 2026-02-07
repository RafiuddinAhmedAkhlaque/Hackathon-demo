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

# Tests for successful operations
def test_math_add_operation(client):
    """Test addition operation"""
    response = client.post('/math', 
                          data=json.dumps({
                              "operation": "add",
                              "a": 10,
                              "b": 5
                          }),
                          content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data["operation"] == "add"
    assert data["a"] == 10
    assert data["b"] == 5
    assert data["result"] == 15

def test_math_subtract_operation(client):
    """Test subtraction operation"""
    response = client.post('/math', 
                          data=json.dumps({
                              "operation": "subtract",
                              "a": 10,
                              "b": 3
                          }),
                          content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data["operation"] == "subtract"
    assert data["a"] == 10
    assert data["b"] == 3
    assert data["result"] == 7

def test_math_multiply_operation(client):
    """Test multiplication operation"""
    response = client.post('/math', 
                          data=json.dumps({
                              "operation": "multiply",
                              "a": 4,
                              "b": 7
                          }),
                          content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data["operation"] == "multiply"
    assert data["a"] == 4
    assert data["b"] == 7
    assert data["result"] == 28

def test_math_divide_operation(client):
    """Test division operation"""
    response = client.post('/math', 
                          data=json.dumps({
                              "operation": "divide",
                              "a": 20,
                              "b": 4
                          }),
                          content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data["operation"] == "divide"
    assert data["a"] == 20
    assert data["b"] == 4
    assert data["result"] == 5

# Tests for decimal/float support
def test_math_add_with_decimals(client):
    """Test addition operation with decimal numbers"""
    response = client.post('/math', 
                          data=json.dumps({
                              "operation": "add",
                              "a": 10.5,
                              "b": 2.3
                          }),
                          content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data["operation"] == "add"
    assert data["a"] == 10.5
    assert data["b"] == 2.3
    assert data["result"] == 12.8

def test_math_divide_with_decimals(client):
    """Test division operation with decimal result"""
    response = client.post('/math', 
                          data=json.dumps({
                              "operation": "divide",
                              "a": 7,
                              "b": 2
                          }),
                          content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data["operation"] == "divide"
    assert data["a"] == 7
    assert data["b"] == 2
    assert data["result"] == 3.5

# Tests for error conditions
def test_math_unsupported_operation(client):
    """Test error response for unsupported operation"""
    response = client.post('/math', 
                          data=json.dumps({
                              "operation": "power",
                              "a": 2,
                              "b": 3
                          }),
                          content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "Unsupported operation" in data["error"]

def test_math_missing_operation_field(client):
    """Test error response when operation field is missing"""
    response = client.post('/math', 
                          data=json.dumps({
                              "a": 10,
                              "b": 5
                          }),
                          content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "Missing required field: operation" in data["error"]

def test_math_missing_a_field(client):
    """Test error response when 'a' field is missing"""
    response = client.post('/math', 
                          data=json.dumps({
                              "operation": "add",
                              "b": 5
                          }),
                          content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "Missing required field: a" in data["error"]

def test_math_missing_b_field(client):
    """Test error response when 'b' field is missing"""
    response = client.post('/math', 
                          data=json.dumps({
                              "operation": "add",
                              "a": 10
                          }),
                          content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "Missing required field: b" in data["error"]

def test_math_divide_by_zero(client):
    """Test error response for division by zero"""
    response = client.post('/math', 
                          data=json.dumps({
                              "operation": "divide",
                              "a": 10,
                              "b": 0
                          }),
                          content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "Cannot divide by zero" in data["error"]

def test_math_invalid_number_a(client):
    """Test error response when 'a' is not a number"""
    response = client.post('/math', 
                          data=json.dumps({
                              "operation": "add",
                              "a": "not_a_number",
                              "b": 5
                          }),
                          content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "must be numbers" in data["error"]

def test_math_invalid_number_b(client):
    """Test error response when 'b' is not a number"""
    response = client.post('/math', 
                          data=json.dumps({
                              "operation": "add",
                              "a": 10,
                              "b": "not_a_number"
                          }),
                          content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "must be numbers" in data["error"]

def test_math_no_json_data(client):
    """Test error response when no JSON data is provided"""
    response = client.post('/math', 
                          data="not json",
                          content_type='text/plain')
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "Request must contain JSON data" in data["error"]

def test_math_empty_json(client):
    """Test error response when empty JSON is provided"""
    response = client.post('/math', 
                          data=json.dumps({}),
                          content_type='application/json')
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "Missing required field: operation" in data["error"]

# Test with negative numbers
def test_math_negative_numbers(client):
    """Test operations with negative numbers"""
    response = client.post('/math', 
                          data=json.dumps({
                              "operation": "add",
                              "a": -5,
                              "b": 3
                          }),
                          content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data["result"] == -2

def test_math_subtract_negative_result(client):
    """Test subtraction that results in negative number"""
    response = client.post('/math', 
                          data=json.dumps({
                              "operation": "subtract",
                              "a": 3,
                              "b": 8
                          }),
                          content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data["result"] == -5

# Test response format
def test_math_response_format(client):
    """Test that the response format matches the specification"""
    response = client.post('/math', 
                          data=json.dumps({
                              "operation": "add",
                              "a": 10,
                              "b": 5
                          }),
                          content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    
    # Check that all required fields are present
    required_fields = ["operation", "a", "b", "result"]
    for field in required_fields:
        assert field in data
    
    # Check that the values match what was sent
    assert data["operation"] == "add"
    assert data["a"] == 10
    assert data["b"] == 5
    assert data["result"] == 15