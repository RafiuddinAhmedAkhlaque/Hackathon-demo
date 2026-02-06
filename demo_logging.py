"""
Demo script to show logging middleware in action
"""
import requests
import time

def test_logging_middleware():
    """Make sample requests to demonstrate logging"""
    base_url = "http://127.0.0.1:5000"
    
    print("Making sample requests to test logging middleware...")
    print("Check the server console output to see the logs.")
    print()
    
    try:
        # Test GET /hello
        print("1. Testing GET /hello")
        response = requests.get(f"{base_url}/hello")
        print(f"   Response: {response.status_code} - {response.json()}")
        time.sleep(0.5)
        
        # Test GET /goodbye
        print("2. Testing GET /goodbye")
        response = requests.get(f"{base_url}/goodbye")
        print(f"   Response: {response.status_code} - {response.json()}")
        time.sleep(0.5)
        
        # Test 404 error
        print("3. Testing GET /nonexistent (404 error)")
        response = requests.get(f"{base_url}/nonexistent")
        print(f"   Response: {response.status_code}")
        
        print()
        print("Demo completed! Check the Flask server console for log entries.")
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to Flask server.")
        print("Please make sure the Flask server is running with 'python app.py'")

if __name__ == "__main__":
    test_logging_middleware()