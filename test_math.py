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
    """Test basic addition operation"""
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
    """Test basic subtraction operation"""
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
    """Test basic multiplication operation"""
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
    """Test basic division operation"""
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

def test_math_with_decimals(client):
    """Test operations with decimal numbers"""
    response = client.post('/math',
                          data=json.dumps({
                              "operation": "add",
                              "a": 3.14,
                              "b": 2.86
                          }),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data["operation"] == "add"
    assert data["a"] == 3.14
    assert data["b"] == 2.86
    assert abs(data["result"] - 6.0) < 0.001  # Using abs for floating point comparison

def test_math_divide_by_zero(client):
    """Test division by zero returns 400 error"""
    response = client.post('/math',
                          data=json.dumps({
                              "operation": "divide",
                              "a": 10,
                              "b": 0
                          }),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = response.get_json()
    assert "Cannot divide by zero" in data["error"]

def test_math_invalid_operation(client):
    """Test invalid operation returns 400 error"""
    response = client.post('/math',
                          data=json.dumps({
                              "operation": "power",
                              "a": 2,
                              "b": 3
                          }),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = response.get_json()
    assert "Operation must be one of" in data["error"]

def test_math_missing_operation(client):
    """Test missing operation field returns 400 error"""
    response = client.post('/math',
                          data=json.dumps({
                              "a": 10,
                              "b": 5
                          }),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = response.get_json()
    assert "Missing required field: operation" in data["error"]

def test_math_missing_a_field(client):
    """Test missing 'a' field returns 400 error"""
    response = client.post('/math',
                          data=json.dumps({
                              "operation": "add",
                              "b": 5
                          }),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = response.get_json()
    assert "Missing required field: a" in data["error"]

def test_math_missing_b_field(client):
    """Test missing 'b' field returns 400 error"""
    response = client.post('/math',
                          data=json.dumps({
                              "operation": "add",
                              "a": 10
                          }),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = response.get_json()
    assert "Missing required field: b" in data["error"]

def test_math_invalid_number_a(client):
    """Test invalid number for 'a' returns 400 error"""
    response = client.post('/math',
                          data=json.dumps({
                              "operation": "add",
                              "a": "not_a_number",
                              "b": 5
                          }),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = response.get_json()
    assert "must be valid numbers" in data["error"]

def test_math_invalid_number_b(client):
    """Test invalid number for 'b' returns 400 error"""
    response = client.post('/math',
                          data=json.dumps({
                              "operation": "add",
                              "a": 10,
                              "b": "not_a_number"
                          }),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = response.get_json()
    assert "must be valid numbers" in data["error"]

def test_math_no_json_data(client):
    """Test request without JSON data returns 400 error"""
    response = client.post('/math')
    
    assert response.status_code == 400
    data = response.get_json()
    assert "Request must contain JSON data" in data["error"]

def test_math_negative_numbers(client):
    """Test operations with negative numbers"""
    response = client.post('/math',
                          data=json.dumps({
                              "operation": "subtract",
                              "a": -5,
                              "b": 3
                          }),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data["result"] == -8

def test_math_string_numbers(client):
    """Test that string representations of numbers are converted correctly"""
    response = client.post('/math',
                          data=json.dumps({
                              "operation": "multiply",
                              "a": "3",
                              "b": "7"
                          }),
                          content_type='application/json')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data["a"] == 3.0
    assert data["b"] == 7.0
    assert data["result"] == 21.0