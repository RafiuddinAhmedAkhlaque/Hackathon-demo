"""Unit tests for greeting API endpoints"""
import pytest
from app import create_app


@pytest.fixture
def client():
    """Create test client"""
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestHelloEndpoints:
    """Test cases for hello endpoints"""

    def test_generic_hello_endpoint(self, client):
        """Test the generic /hello endpoint returns Hello, World!"""
        response = client.get('/hello')
        
        assert response.status_code == 200
        assert response.is_json
        data = response.get_json()
        assert data['message'] == "Hello, World!"

    def test_personalized_hello_valid_name(self, client):
        """Test personalized greeting with valid name"""
        response = client.get('/hello/Alice')
        
        assert response.status_code == 200
        assert response.is_json
        data = response.get_json()
        assert data['message'] == "Hello, Alice!"

    def test_personalized_hello_valid_name_with_spaces(self, client):
        """Test personalized greeting with name containing spaces"""
        # URL encoding: spaces become %20
        response = client.get('/hello/Alice%20Smith')
        
        assert response.status_code == 200
        assert response.is_json
        data = response.get_json()
        assert data['message'] == "Hello, Alice Smith!"

    def test_personalized_hello_valid_name_with_special_chars(self, client):
        """Test personalized greeting with name containing apostrophe"""
        response = client.get("/hello/O'Connor")
        
        assert response.status_code == 200
        assert response.is_json
        data = response.get_json()
        assert data['message'] == "Hello, O'Connor!"

    def test_personalized_hello_empty_string(self, client):
        """Test personalized greeting with empty string returns 400"""
        # Empty string after /hello/
        response = client.get('/hello/')
        
        # Flask will redirect /hello/ to /hello if no trailing slash rule exists
        # But our route expects a name parameter, so this should be 404
        # Let's test with an explicit empty string encoded
        response = client.get('/hello/%20')  # URL encoded space
        
        assert response.status_code == 400
        assert response.is_json
        data = response.get_json()
        assert 'error' in data
        assert 'Name cannot be empty' in data['error']

    def test_personalized_hello_name_with_numbers(self, client):
        """Test personalized greeting with name containing numbers returns 400"""
        response = client.get('/hello/Alice123')
        
        assert response.status_code == 400
        assert response.is_json
        data = response.get_json()
        assert 'error' in data
        assert 'Name cannot contain numbers' in data['error']

    def test_personalized_hello_name_all_numbers(self, client):
        """Test personalized greeting with name that is all numbers returns 400"""
        response = client.get('/hello/12345')
        
        assert response.status_code == 400
        assert response.is_json
        data = response.get_json()
        assert 'error' in data
        assert 'Name cannot contain numbers' in data['error']

    def test_personalized_hello_name_with_mixed_numbers(self, client):
        """Test personalized greeting with name containing mixed letters and numbers"""
        response = client.get('/hello/John2Doe')
        
        assert response.status_code == 400
        assert response.is_json
        data = response.get_json()
        assert 'error' in data
        assert 'Name cannot contain numbers' in data['error']

    def test_health_endpoint(self, client):
        """Test health endpoint is working"""
        response = client.get('/health')
        
        assert response.status_code == 200
        assert response.is_json
        data = response.get_json()
        assert data['status'] == 'healthy'
        assert data['service'] == 'greeting-api'


class TestEdgeCases:
    """Test edge cases for the greeting API"""

    def test_very_long_name(self, client):
        """Test with very long name"""
        long_name = "A" * 100
        response = client.get(f'/hello/{long_name}')
        
        assert response.status_code == 200
        assert response.is_json
        data = response.get_json()
        assert data['message'] == f"Hello, {long_name}!"

    def test_unicode_name(self, client):
        """Test with unicode characters in name"""
        # Testing with accented characters
        response = client.get('/hello/José')
        
        assert response.status_code == 200
        assert response.is_json
        data = response.get_json()
        assert data['message'] == "Hello, José!"

    def test_name_with_only_whitespace(self, client):
        """Test with name that contains only whitespace"""
        response = client.get('/hello/%20%20%20')  # Three spaces URL encoded
        
        assert response.status_code == 400
        assert response.is_json
        data = response.get_json()
        assert 'error' in data
        assert 'Name cannot be empty' in data['error']