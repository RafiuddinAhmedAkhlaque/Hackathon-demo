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

class TestMathEndpointOperations:
    """Test all math operations"""
    
    def test_add_operation(self, client):
        """Test addition operation"""
        data = {
            "operation": "add",
            "a": 10,
            "b": 5
        }
        response = client.post('/math', 
                             data=json.dumps(data), 
                             content_type='application/json')
        
        assert response.status_code == 200
        result = response.get_json()
        assert result["operation"] == "add"
        assert result["a"] == 10
        assert result["b"] == 5
        assert result["result"] == 15
    
    def test_subtract_operation(self, client):
        """Test subtraction operation"""
        data = {
            "operation": "subtract",
            "a": 10,
            "b": 3
        }
        response = client.post('/math', 
                             data=json.dumps(data), 
                             content_type='application/json')
        
        assert response.status_code == 200
        result = response.get_json()
        assert result["operation"] == "subtract"
        assert result["a"] == 10
        assert result["b"] == 3
        assert result["result"] == 7
    
    def test_multiply_operation(self, client):
        """Test multiplication operation"""
        data = {
            "operation": "multiply",
            "a": 4,
            "b": 6
        }
        response = client.post('/math', 
                             data=json.dumps(data), 
                             content_type='application/json')
        
        assert response.status_code == 200
        result = response.get_json()
        assert result["operation"] == "multiply"
        assert result["a"] == 4
        assert result["b"] == 6
        assert result["result"] == 24
    
    def test_divide_operation(self, client):
        """Test division operation"""
        data = {
            "operation": "divide",
            "a": 15,
            "b": 3
        }
        response = client.post('/math', 
                             data=json.dumps(data), 
                             content_type='application/json')
        
        assert response.status_code == 200
        result = response.get_json()
        assert result["operation"] == "divide"
        assert result["a"] == 15
        assert result["b"] == 3
        assert result["result"] == 5

class TestMathEndpointFloatSupport:
    """Test float/decimal number support"""
    
    def test_add_with_floats(self, client):
        """Test addition with float numbers"""
        data = {
            "operation": "add",
            "a": 10.5,
            "b": 3.2
        }
        response = client.post('/math', 
                             data=json.dumps(data), 
                             content_type='application/json')
        
        assert response.status_code == 200
        result = response.get_json()
        assert result["result"] == pytest.approx(13.7, rel=1e-9)
    
    def test_divide_with_floats(self, client):
        """Test division with float numbers"""
        data = {
            "operation": "divide",
            "a": 7.5,
            "b": 2.5
        }
        response = client.post('/math', 
                             data=json.dumps(data), 
                             content_type='application/json')
        
        assert response.status_code == 200
        result = response.get_json()
        assert result["result"] == pytest.approx(3.0, rel=1e-9)
    
    def test_mixed_int_and_float(self, client):
        """Test operations with mixed integer and float"""
        data = {
            "operation": "multiply",
            "a": 5,
            "b": 2.5
        }
        response = client.post('/math', 
                             data=json.dumps(data), 
                             content_type='application/json')
        
        assert response.status_code == 200
        result = response.get_json()
        assert result["result"] == pytest.approx(12.5, rel=1e-9)

class TestMathEndpointErrorHandling:
    """Test error handling scenarios"""
    
    def test_unsupported_operation(self, client):
        """Test unsupported operation returns 400"""
        data = {
            "operation": "power",
            "a": 5,
            "b": 2
        }
        response = client.post('/math', 
                             data=json.dumps(data), 
                             content_type='application/json')
        
        assert response.status_code == 400
        result = response.get_json()
        assert "error" in result
        assert "Unsupported operation" in result["error"]
    
    def test_missing_operation_field(self, client):
        """Test missing operation field returns 400"""
        data = {
            "a": 5,
            "b": 2
        }
        response = client.post('/math', 
                             data=json.dumps(data), 
                             content_type='application/json')
        
        assert response.status_code == 400
        result = response.get_json()
        assert "error" in result
        assert "Missing required field: operation" in result["error"]
    
    def test_missing_a_field(self, client):
        """Test missing 'a' field returns 400"""
        data = {
            "operation": "add",
            "b": 5
        }
        response = client.post('/math', 
                             data=json.dumps(data), 
                             content_type='application/json')
        
        assert response.status_code == 400
        result = response.get_json()
        assert "error" in result
        assert "Missing required field: a" in result["error"]
    
    def test_missing_b_field(self, client):
        """Test missing 'b' field returns 400"""
        data = {
            "operation": "add",
            "a": 5
        }
        response = client.post('/math', 
                             data=json.dumps(data), 
                             content_type='application/json')
        
        assert response.status_code == 400
        result = response.get_json()
        assert "error" in result
        assert "Missing required field: b" in result["error"]
    
    def test_divide_by_zero(self, client):
        """Test divide by zero returns 400 with specific message"""
        data = {
            "operation": "divide",
            "a": 10,
            "b": 0
        }
        response = client.post('/math', 
                             data=json.dumps(data), 
                             content_type='application/json')
        
        assert response.status_code == 400
        result = response.get_json()
        assert "error" in result
        assert result["error"] == "Cannot divide by zero"
    
    def test_invalid_number_type_for_a(self, client):
        """Test invalid number type for 'a' returns 400"""
        data = {
            "operation": "add",
            "a": "not_a_number",
            "b": 5
        }
        response = client.post('/math', 
                             data=json.dumps(data), 
                             content_type='application/json')
        
        assert response.status_code == 400
        result = response.get_json()
        assert "error" in result
        assert "must be valid numbers" in result["error"]
    
    def test_invalid_number_type_for_b(self, client):
        """Test invalid number type for 'b' returns 400"""
        data = {
            "operation": "add",
            "a": 5,
            "b": "not_a_number"
        }
        response = client.post('/math', 
                             data=json.dumps(data), 
                             content_type='application/json')
        
        assert response.status_code == 400
        result = response.get_json()
        assert "error" in result
        assert "must be valid numbers" in result["error"]
    
    def test_no_json_body(self, client):
        """Test request without JSON body returns 400"""
        response = client.post('/math', content_type='application/json')
        
        assert response.status_code == 400
        result = response.get_json()
        assert "error" in result
        assert "Request body must be valid JSON" in result["error"]
    
    def test_empty_json_body(self, client):
        """Test request with empty JSON body returns 400"""
        response = client.post('/math', 
                             data=json.dumps({}), 
                             content_type='application/json')
        
        assert response.status_code == 400
        result = response.get_json()
        assert "error" in result
        assert "Missing required field: operation" in result["error"]

class TestMathEndpointEdgeCases:
    """Test edge cases"""
    
    def test_negative_numbers(self, client):
        """Test operations with negative numbers"""
        data = {
            "operation": "add",
            "a": -5,
            "b": 3
        }
        response = client.post('/math', 
                             data=json.dumps(data), 
                             content_type='application/json')
        
        assert response.status_code == 200
        result = response.get_json()
        assert result["result"] == -2
    
    def test_zero_values(self, client):
        """Test operations with zero values"""
        data = {
            "operation": "multiply",
            "a": 0,
            "b": 100
        }
        response = client.post('/math', 
                             data=json.dumps(data), 
                             content_type='application/json')
        
        assert response.status_code == 200
        result = response.get_json()
        assert result["result"] == 0
    
    def test_large_numbers(self, client):
        """Test operations with large numbers"""
        data = {
            "operation": "add",
            "a": 1000000,
            "b": 2000000
        }
        response = client.post('/math', 
                             data=json.dumps(data), 
                             content_type='application/json')
        
        assert response.status_code == 200
        result = response.get_json()
        assert result["result"] == 3000000

class TestMathEndpointResponseFormat:
    """Test response format requirements"""
    
    def test_response_contains_all_required_fields(self, client):
        """Test that successful response contains all required fields"""
        data = {
            "operation": "add",
            "a": 10,
            "b": 5
        }
        response = client.post('/math', 
                             data=json.dumps(data), 
                             content_type='application/json')
        
        assert response.status_code == 200
        result = response.get_json()
        
        # Check all required fields are present
        required_fields = ["operation", "a", "b", "result"]
        for field in required_fields:
            assert field in result
        
        # Check field values match expected format
        assert isinstance(result["operation"], str)
        assert isinstance(result["a"], (int, float))
        assert isinstance(result["b"], (int, float))
        assert isinstance(result["result"], (int, float))