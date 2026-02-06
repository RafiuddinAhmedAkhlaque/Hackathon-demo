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

class TestMathEndpoint:
    """Test class for the /math endpoint"""
    
    def test_math_add_operation(self, client):
        """Test addition operation"""
        data = {"operation": "add", "a": 10, "b": 5}
        response = client.post('/math', 
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 200
        result = response.get_json()
        assert result["operation"] == "add"
        assert result["a"] == 10
        assert result["b"] == 5
        assert result["result"] == 15
    
    def test_math_subtract_operation(self, client):
        """Test subtraction operation"""
        data = {"operation": "subtract", "a": 10, "b": 3}
        response = client.post('/math', 
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 200
        result = response.get_json()
        assert result["operation"] == "subtract"
        assert result["a"] == 10
        assert result["b"] == 3
        assert result["result"] == 7
    
    def test_math_multiply_operation(self, client):
        """Test multiplication operation"""
        data = {"operation": "multiply", "a": 4, "b": 6}
        response = client.post('/math', 
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 200
        result = response.get_json()
        assert result["operation"] == "multiply"
        assert result["a"] == 4
        assert result["b"] == 6
        assert result["result"] == 24
    
    def test_math_divide_operation(self, client):
        """Test division operation"""
        data = {"operation": "divide", "a": 15, "b": 3}
        response = client.post('/math', 
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 200
        result = response.get_json()
        assert result["operation"] == "divide"
        assert result["a"] == 15
        assert result["b"] == 3
        assert result["result"] == 5
    
    def test_math_with_decimal_numbers(self, client):
        """Test operations with decimal numbers"""
        data = {"operation": "add", "a": 10.5, "b": 2.7}
        response = client.post('/math', 
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 200
        result = response.get_json()
        assert result["operation"] == "add"
        assert result["a"] == 10.5
        assert result["b"] == 2.7
        assert abs(result["result"] - 13.2) < 0.0001  # Handle floating point precision
    
    def test_math_division_with_decimal_result(self, client):
        """Test division resulting in decimal"""
        data = {"operation": "divide", "a": 10, "b": 3}
        response = client.post('/math', 
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 200
        result = response.get_json()
        assert result["operation"] == "divide"
        assert result["a"] == 10
        assert result["b"] == 3
        assert abs(result["result"] - 3.333333333333333) < 0.0001
    
    def test_math_invalid_operation(self, client):
        """Test invalid operation returns 400"""
        data = {"operation": "power", "a": 10, "b": 5}
        response = client.post('/math', 
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 400
        result = response.get_json()
        assert "error" in result
        assert "Invalid operation" in result["error"]
    
    def test_math_missing_operation_field(self, client):
        """Test missing operation field returns 400"""
        data = {"a": 10, "b": 5}
        response = client.post('/math', 
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 400
        result = response.get_json()
        assert "error" in result
        assert "Missing required field: operation" in result["error"]
    
    def test_math_missing_a_field(self, client):
        """Test missing 'a' field returns 400"""
        data = {"operation": "add", "b": 5}
        response = client.post('/math', 
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 400
        result = response.get_json()
        assert "error" in result
        assert "Missing required field: a" in result["error"]
    
    def test_math_missing_b_field(self, client):
        """Test missing 'b' field returns 400"""
        data = {"operation": "add", "a": 10}
        response = client.post('/math', 
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 400
        result = response.get_json()
        assert "error" in result
        assert "Missing required field: b" in result["error"]
    
    def test_math_divide_by_zero(self, client):
        """Test division by zero returns 400 with specific message"""
        data = {"operation": "divide", "a": 10, "b": 0}
        response = client.post('/math', 
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 400
        result = response.get_json()
        assert "error" in result
        assert result["error"] == "Cannot divide by zero"
    
    def test_math_invalid_number_a(self, client):
        """Test invalid number for 'a' returns 400"""
        data = {"operation": "add", "a": "not_a_number", "b": 5}
        response = client.post('/math', 
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 400
        result = response.get_json()
        assert "error" in result
        assert "must be numbers" in result["error"]
    
    def test_math_invalid_number_b(self, client):
        """Test invalid number for 'b' returns 400"""
        data = {"operation": "add", "a": 10, "b": "not_a_number"}
        response = client.post('/math', 
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 400
        result = response.get_json()
        assert "error" in result
        assert "must be numbers" in result["error"]
    
    def test_math_empty_json_body(self, client):
        """Test empty JSON body returns 400"""
        response = client.post('/math', 
                             data='{}',
                             content_type='application/json')
        
        assert response.status_code == 400
        result = response.get_json()
        assert "error" in result
        assert "Missing required field: operation" in result["error"]
    
    def test_math_no_json_body(self, client):
        """Test request with no JSON body returns 400"""
        response = client.post('/math')
        
        assert response.status_code == 400
        result = response.get_json()
        assert "error" in result
        assert "Request body must be valid JSON" in result["error"]
    
    def test_math_malformed_json(self, client):
        """Test malformed JSON returns 400"""
        response = client.post('/math', 
                             data='{"operation": "add", "a": 10, "b":}',  # Invalid JSON
                             content_type='application/json')
        
        assert response.status_code == 400
        result = response.get_json()
        assert "error" in result
        assert "Request body must be valid JSON" in result["error"]
    
    def test_math_negative_numbers(self, client):
        """Test operations with negative numbers"""
        data = {"operation": "subtract", "a": -5, "b": 3}
        response = client.post('/math', 
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 200
        result = response.get_json()
        assert result["operation"] == "subtract"
        assert result["a"] == -5
        assert result["b"] == 3
        assert result["result"] == -8
    
    def test_math_zero_values(self, client):
        """Test operations with zero values"""
        data = {"operation": "multiply", "a": 0, "b": 100}
        response = client.post('/math', 
                             data=json.dumps(data),
                             content_type='application/json')
        
        assert response.status_code == 200
        result = response.get_json()
        assert result["operation"] == "multiply"
        assert result["a"] == 0
        assert result["b"] == 100
        assert result["result"] == 0