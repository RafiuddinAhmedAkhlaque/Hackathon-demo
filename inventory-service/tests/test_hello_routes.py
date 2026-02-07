"""Tests for hello routes."""
import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app import create_app


@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


class TestHelloRoutes:
    """Test cases for hello endpoints."""

    def test_hello_generic(self, client):
        """Test generic hello endpoint returns correct message."""
        response = client.get('/hello')
        assert response.status_code == 200
        assert response.json == {"message": "Hello, World!"}

    def test_hello_with_valid_name(self, client):
        """Test personalized hello with valid name."""
        response = client.get('/hello/Alice')
        assert response.status_code == 200
        assert response.json == {"message": "Hello, Alice!"}

    def test_hello_with_another_valid_name(self, client):
        """Test personalized hello with another valid name."""
        response = client.get('/hello/Bob')
        assert response.status_code == 200
        assert response.json == {"message": "Hello, Bob!"}

    def test_hello_with_name_containing_spaces(self, client):
        """Test personalized hello with name containing spaces."""
        response = client.get('/hello/John Doe')
        assert response.status_code == 200
        assert response.json == {"message": "Hello, John Doe!"}

    def test_hello_with_empty_name(self, client):
        """Test hello with empty name returns 400 error."""
        # URL with empty string
        response = client.get('/hello/')
        # This will hit the generic route, not the parameterized one
        # We need to test with a space or something that gets stripped
        response = client.get('/hello/ ')
        assert response.status_code == 400
        assert "error" in response.json
        assert "empty" in response.json["error"].lower()

    def test_hello_with_name_containing_numbers(self, client):
        """Test hello with name containing numbers returns 400 error."""
        response = client.get('/hello/Alice123')
        assert response.status_code == 400
        assert "error" in response.json
        assert "numbers" in response.json["error"].lower()

    def test_hello_with_name_starting_with_number(self, client):
        """Test hello with name starting with number returns 400 error."""
        response = client.get('/hello/123Alice')
        assert response.status_code == 400
        assert "error" in response.json
        assert "numbers" in response.json["error"].lower()

    def test_hello_with_name_mixed_numbers(self, client):
        """Test hello with name having numbers in middle returns 400 error."""
        response = client.get('/hello/Al1ce')
        assert response.status_code == 400
        assert "error" in response.json
        assert "numbers" in response.json["error"].lower()

    def test_hello_with_special_characters(self, client):
        """Test hello with name containing special characters (should work)."""
        response = client.get('/hello/Alice-Marie')
        assert response.status_code == 200
        assert response.json == {"message": "Hello, Alice-Marie!"}

    def test_hello_with_apostrophe(self, client):
        """Test hello with name containing apostrophe (should work)."""
        response = client.get("/hello/O'Connor")
        assert response.status_code == 200
        assert response.json == {"message": "Hello, O'Connor!"}