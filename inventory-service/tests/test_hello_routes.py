"""Tests for hello endpoints."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from app import create_app


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_hello_generic(client):
    """Test the generic /hello endpoint."""
    response = client.get('/hello')
    assert response.status_code == 200
    data = response.get_json()
    assert data == {"message": "Hello, World!"}


def test_hello_personalized_valid_name(client):
    """Test the personalized /hello/<name> endpoint with a valid name."""
    response = client.get('/hello/Alice')
    assert response.status_code == 200
    data = response.get_json()
    assert data == {"message": "Hello, Alice!"}


def test_hello_personalized_another_valid_name(client):
    """Test the personalized /hello/<name> endpoint with another valid name."""
    response = client.get('/hello/Bob')
    assert response.status_code == 200
    data = response.get_json()
    assert data == {"message": "Hello, Bob!"}


def test_hello_personalized_name_with_spaces(client):
    """Test the personalized /hello/<name> endpoint with a name containing spaces."""
    response = client.get('/hello/John Doe')
    assert response.status_code == 200
    data = response.get_json()
    assert data == {"message": "Hello, John Doe!"}


def test_hello_personalized_empty_name(client):
    """Test the personalized /hello/<name> endpoint with an empty name."""
    # Flask handles empty path parameters as missing routes, so we test with just spaces
    response = client.get('/hello/   ')  # Only spaces
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "Name cannot be empty" in data["error"]


def test_hello_personalized_name_with_numbers(client):
    """Test the personalized /hello/<name> endpoint with a name containing numbers."""
    response = client.get('/hello/Alice123')
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "Name cannot contain numbers" in data["error"]


def test_hello_personalized_name_with_numbers_in_middle(client):
    """Test the personalized /hello/<name> endpoint with numbers in the middle of name."""
    response = client.get('/hello/Al1ce')
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "Name cannot contain numbers" in data["error"]


def test_hello_personalized_name_starting_with_number(client):
    """Test the personalized /hello/<name> endpoint with name starting with a number."""
    response = client.get('/hello/1Alice')
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
    assert "Name cannot contain numbers" in data["error"]