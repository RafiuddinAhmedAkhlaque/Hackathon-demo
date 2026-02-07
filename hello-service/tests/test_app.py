"""Tests for Hello Service"""
import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestHelloEndpoint:
    """Tests for the generic /hello endpoint"""
    
    def test_hello_returns_hello_world(self, client):
        """Test that /hello returns the correct generic message"""
        response = client.get('/hello')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data == {"message": "Hello, World!"}


class TestPersonalizedHelloEndpoint:
    """Tests for the personalized /hello/<name> endpoint"""
    
    def test_hello_with_valid_name(self, client):
        """Test that /hello/<name> returns personalized greeting for valid names"""
        test_cases = [
            ("Alice", "Hello, Alice!"),
            ("Bob", "Hello, Bob!"),
            ("John-Doe", "Hello, John-Doe!"),  # Allow hyphens
            ("Mary Jane", "Hello, Mary Jane!"),  # Allow spaces
            ("José", "Hello, José!"),  # Allow accented characters
        ]
        
        for name, expected_message in test_cases:
            response = client.get(f'/hello/{name}')
            assert response.status_code == 200
            
            data = response.get_json()
            assert data == {"message": expected_message}
    
    def test_hello_with_name_containing_numbers_returns_400(self, client):
        """Test that names containing numbers return 400 error"""
        test_cases = [
            "Alice123",
            "Bob2",
            "John3Doe",
            "123Alice",
            "Al1ce"
        ]
        
        for name in test_cases:
            response = client.get(f'/hello/{name}')
            assert response.status_code == 400
            
            data = response.get_json()
            assert data == {"error": "Name cannot contain numbers"}
    
    def test_hello_with_empty_name_returns_400(self, client):
        """Test that empty names return 400 error"""
        # Test with empty string (this might be tricky to test via URL)
        # The Flask route won't match empty string, so we need to test with spaces
        test_cases = [
            "%20",  # Single space (URL encoded)
            "%20%20%20",  # Multiple spaces (URL encoded)
        ]
        
        for name in test_cases:
            response = client.get(f'/hello/{name}')
            assert response.status_code == 400
            
            data = response.get_json()
            assert data == {"error": "Name cannot be empty"}
    
    def test_hello_with_only_spaces_returns_400(self, client):
        """Test that names with only spaces return 400 error"""
        # Test with URL-encoded spaces
        response = client.get('/hello/ ')  # Single space
        assert response.status_code == 400
        
        data = response.get_json()
        assert data == {"error": "Name cannot be empty"}


class TestHealthEndpoint:
    """Tests for the health check endpoint"""
    
    def test_health_check(self, client):
        """Test that health endpoint returns correct status"""
        response = client.get('/health')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data == {"status": "healthy", "service": "hello-service"}