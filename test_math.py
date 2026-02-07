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
                              "b": 6
                          }),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data["operation"] == "multiply"
    assert data["a"] == 4
    assert data["b"] == 6
    assert data["result"] == 24

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

# Test floating point numbers
def test_math_add_floats(client):
    """Test addition with floating point numbers"""
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

def test_math_divide_floats(client):
    """Test division with floating point result"""
    response = client.post('/math',
                          data=json.dumps({
                              "operation": "divide",
                              "a": 10,
                              "b": 3
                          }),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data["operation"] == "divide"
    assert data["a"] == 10
    assert data["b"] == 3
    assert abs(data["result"] - 3.333333333333333) < 1e-10

# Test error cases
def test_math_unsupported_operation(client):
    """Test unsupported operation returns 400"""
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
    """Test missing operation field returns 400"""
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
    """Test missing 'a' field returns 400"""
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
    """Test missing 'b' field returns 400"""
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
    """Test division by zero returns 400 with specific message"""
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
    assert data["error"] == "Cannot divide by zero"

def test_math_invalid_number_a(client):
    """Test invalid number for 'a' field returns 400"""
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
    """Test invalid number for 'b' field returns 400"""
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
    """Test request without JSON data returns 400"""
    response = client.post('/math')
    
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "Request must contain JSON data" in data["error"]

def test_math_empty_json(client):
    """Test empty JSON object returns 400"""
    response = client.post('/math',
                          data=json.dumps({}),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "Missing required field: operation" in data["error"]

# Test negative numbers
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
    """Test subtraction resulting in negative number"""
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

# Test string numbers (should be converted to floats)
def test_math_string_numbers(client):
    """Test that string numbers are converted to floats"""
    response = client.post('/math',
                          data=json.dumps({
                              "operation": "multiply",
                              "a": "2.5",
                              "b": "4"
                          }),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data["a"] == 2.5
    assert data["b"] == 4.0
    assert data["result"] == 10.0