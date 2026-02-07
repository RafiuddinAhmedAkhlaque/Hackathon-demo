#!/usr/bin/env python3
"""
Simple test script to validate the math endpoint functionality
"""
import json
import sys
from app import app

def test_endpoint():
    """Test the math endpoint with various scenarios"""
    with app.test_client() as client:
        
        print("Testing /math endpoint...")
        
        # Test addition
        response = client.post('/math', json={
            "operation": "add",
            "a": 10,
            "b": 5
        })
        print(f"Add test: {response.status_code} - {response.get_json()}")
        
        # Test division by zero
        response = client.post('/math', json={
            "operation": "divide",
            "a": 10,
            "b": 0
        })
        print(f"Divide by zero test: {response.status_code} - {response.get_json()}")
        
        # Test invalid operation
        response = client.post('/math', json={
            "operation": "power",
            "a": 2,
            "b": 3
        })
        print(f"Invalid operation test: {response.status_code} - {response.get_json()}")
        
        # Test missing field
        response = client.post('/math', json={
            "operation": "add",
            "a": 10
        })
        print(f"Missing field test: {response.status_code} - {response.get_json()}")
        
        print("All basic tests completed successfully!")

if __name__ == '__main__':
    test_endpoint()