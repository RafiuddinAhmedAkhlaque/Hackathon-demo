"""Tests for hello routes."""
import pytest
from app import create_app


class TestHelloRoutes:
    """Test cases for hello endpoints."""

    @pytest.fixture
    def app(self):
        """Create application fixture."""
        return create_app()

    @pytest.fixture
    def client(self, app):
        """Create test client fixture."""
        return app.test_client()

    def test_generic_hello_endpoint(self, client):
        """Test the generic /hello endpoint."""
        response = client.get('/hello/')
        assert response.status_code == 200
        assert response.json == {"message": "Hello, World!"}

    def test_personalized_hello_valid_name(self, client):
        """Test personalized greeting with valid name."""
        response = client.get('/hello/Alice')
        assert response.status_code == 200
        assert response.json == {"message": "Hello, Alice!"}

    def test_personalized_hello_another_valid_name(self, client):
        """Test personalized greeting with another valid name."""
        response = client.get('/hello/Bob')
        assert response.status_code == 200
        assert response.json == {"message": "Hello, Bob!"}

    def test_personalized_hello_name_with_spaces(self, client):
        """Test personalized greeting with name containing spaces."""
        response = client.get('/hello/John%20Doe')
        assert response.status_code == 200
        assert response.json == {"message": "Hello, John Doe!"}

    def test_personalized_hello_empty_name(self, client):
        """Test personalized greeting with empty name."""
        response = client.get('/hello/')
        # This should hit the generic endpoint, not the personalized one
        assert response.status_code == 200
        assert response.json == {"message": "Hello, World!"}

    def test_personalized_hello_whitespace_only_name(self, client):
        """Test personalized greeting with whitespace-only name."""
        response = client.get('/hello/%20%20%20')  # URL encoded spaces
        assert response.status_code == 400
        assert "error" in response.json
        assert "empty" in response.json["error"]

    def test_personalized_hello_name_with_numbers(self, client):
        """Test personalized greeting with name containing numbers."""
        response = client.get('/hello/Alice123')
        assert response.status_code == 400
        assert response.json == {"error": "Name cannot contain numbers"}

    def test_personalized_hello_name_with_numbers_in_middle(self, client):
        """Test personalized greeting with numbers in middle of name."""
        response = client.get('/hello/Al1ce')
        assert response.status_code == 400
        assert response.json == {"error": "Name cannot contain numbers"}

    def test_personalized_hello_numeric_name(self, client):
        """Test personalized greeting with purely numeric name."""
        response = client.get('/hello/123')
        assert response.status_code == 400
        assert response.json == {"error": "Name cannot contain numbers"}

    def test_personalized_hello_special_characters(self, client):
        """Test personalized greeting with special characters (should work)."""
        response = client.get('/hello/Mary-Jane')
        assert response.status_code == 200
        assert response.json == {"message": "Hello, Mary-Jane!"}