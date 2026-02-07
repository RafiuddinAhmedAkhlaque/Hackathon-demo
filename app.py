"""
Flask application with hello endpoint
"""
import logging
import time
from flask import Flask, jsonify, request, g

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.before_request
def before_request():
    """Record request start time for duration calculation"""
    g.request_start_time = time.time()

@app.after_request
def after_request(response):
    """Log request details after processing"""
    if hasattr(g, 'request_start_time'):
        # Calculate request duration in milliseconds
        duration_ms = (time.time() - g.request_start_time) * 1000
        
        # Log request details
        logger.info(
            "Request: %s %s - Status: %d - Duration: %.2f ms",
            request.method,
            request.path,
            response.status_code,
            duration_ms
        )
    
    return response

@app.route('/hello', methods=['GET'])
def hello():
    """Hello endpoint that returns a greeting message"""
    return jsonify({"message": "Hello, World!"})

@app.route('/goodbye', methods=['GET'])
def goodbye():
    """Goodbye endpoint that returns a farewell message"""
    return jsonify({"message": "Goodbye, World!"})

@app.route('/math', methods=['POST'])
def math_operation():
    """Math endpoint that performs basic arithmetic operations"""
    try:
        # Get JSON data from request
        data = request.get_json(force=True, silent=True)
        
        # Check if request has JSON data
        if data is None:
            return jsonify({"error": "Request must contain JSON data"}), 400
        
        # Check for required fields
        if 'operation' not in data:
            return jsonify({"error": "Missing required field: operation"}), 400
        
        if 'a' not in data:
            return jsonify({"error": "Missing required field: a"}), 400
            
        if 'b' not in data:
            return jsonify({"error": "Missing required field: b"}), 400
        
        operation = data['operation']
        a = data['a']
        b = data['b']
        
        # Validate that a and b are numbers
        try:
            a = float(a)
            b = float(b)
        except (ValueError, TypeError):
            return jsonify({"error": "Fields 'a' and 'b' must be numbers"}), 400
        
        # Perform the calculation based on operation
        if operation == 'add':
            result = a + b
        elif operation == 'subtract':
            result = a - b
        elif operation == 'multiply':
            result = a * b
        elif operation == 'divide':
            if b == 0:
                return jsonify({"error": "Cannot divide by zero"}), 400
            result = a / b
        else:
            return jsonify({"error": "Unsupported operation. Supported operations are: add, subtract, multiply, divide"}), 400
        
        # Return the result
        response = {
            "operation": operation,
            "a": a,
            "b": b,
            "result": result
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error("Error in math endpoint: %s", str(e))
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)