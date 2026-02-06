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

# Test decimal number support
def test_math_with_decimals(client):
    """Test that operations work with decimal numbers"""
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

def test_math_divide_decimals(client):
    """Test division with decimal result"""
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
    assert abs(data["result"] - 3.3333333333333335) < 1e-10  # Handle floating point precision

# Test error cases - unsupported operations
def test_math_unsupported_operation(client):
    """Test that unsupported operations return 400"""
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
    assert "not supported" in data["error"]

def test_math_empty_operation(client):
    """Test that empty operation returns 400"""
    response = client.post('/math',
                          data=json.dumps({
                              "operation": "",
                              "a": 2,
                              "b": 3
                          }),
                          content_type='application/json')
    
    assert response.status_code == 400

# Test error cases - missing fields
def test_math_missing_operation(client):
    """Test that missing operation field returns 400"""
    response = client.post('/math',
                          data=json.dumps({
                              "a": 10,
                              "b": 5
                          }),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "operation" in data["error"]
    assert "required" in data["error"]

def test_math_missing_a_field(client):
    """Test that missing 'a' field returns 400"""
    response = client.post('/math',
                          data=json.dumps({
                              "operation": "add",
                              "b": 5
                          }),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "'a'" in data["error"]
    assert "required" in data["error"]

def test_math_missing_b_field(client):
    """Test that missing 'b' field returns 400"""
    response = client.post('/math',
                          data=json.dumps({
                              "operation": "add",
                              "a": 10
                          }),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "'b'" in data["error"]
    assert "required" in data["error"]

# Test error cases - division by zero
def test_math_divide_by_zero(client):
    """Test that division by zero returns 400 with specific message"""
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

def test_math_divide_by_zero_with_decimals(client):
    """Test that division by zero with decimals returns 400"""
    response = client.post('/math',
                          data=json.dumps({
                              "operation": "divide",
                              "a": 5.5,
                              "b": 0.0
                          }),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Cannot divide by zero"

# Test error cases - invalid input types
def test_math_invalid_number_format(client):
    """Test that invalid number formats return 400"""
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
    assert "valid numbers" in data["error"]

def test_math_null_values(client):
    """Test that null values return 400"""
    response = client.post('/math',
                          data=json.dumps({
                              "operation": "add",
                              "a": None,
                              "b": 5
                          }),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "valid numbers" in data["error"]

# Test edge cases - empty body
def test_math_empty_body(client):
    """Test that empty request body returns 400"""
    response = client.post('/math',
                          data='',
                          content_type='application/json')
    
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "Request body is required" in data["error"]

def test_math_no_json_body(client):
    """Test that no JSON body returns 400"""
    response = client.post('/math')
    
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "Request body is required" in data["error"]

# Test large numbers
def test_math_large_numbers(client):
    """Test operations with large numbers"""
    response = client.post('/math',
                          data=json.dumps({
                              "operation": "multiply",
                              "a": 999999.99,
                              "b": 1000000.01
                          }),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data["operation"] == "multiply"
    assert data["a"] == 999999.99
    assert data["b"] == 1000000.01
    expected_result = 999999.99 * 1000000.01
    assert abs(data["result"] - expected_result) < 1e-5  # Handle floating point precision

# Test negative numbers
def test_math_negative_numbers(client):
    """Test operations with negative numbers"""
    response = client.post('/math',
                          data=json.dumps({
                              "operation": "subtract",
                              "a": -10,
                              "b": -5
                          }),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data["operation"] == "subtract"
    assert data["a"] == -10
    assert data["b"] == -5
    assert data["result"] == -5  # -10 - (-5) = -5