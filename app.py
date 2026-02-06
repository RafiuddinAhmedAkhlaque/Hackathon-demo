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
def math():
    """Math endpoint that performs basic arithmetic operations"""
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Validate JSON payload exists
        if data is None:
            return jsonify({"error": "Request body must be valid JSON"}), 400
        
        # Check for required fields
        if 'operation' not in data:
            return jsonify({"error": "Missing required field: operation"}), 400
        if 'a' not in data:
            return jsonify({"error": "Missing required field: a"}), 400
        if 'b' not in data:
            return jsonify({"error": "Missing required field: b"}), 400
        
        operation = data['operation']
        
        # Validate operation type
        valid_operations = ['add', 'subtract', 'multiply', 'divide']
        if operation not in valid_operations:
            return jsonify({"error": f"Invalid operation. Supported operations: {', '.join(valid_operations)}"}), 400
        
        # Extract and validate numbers
        try:
            a = float(data['a'])
            b = float(data['b'])
        except (ValueError, TypeError):
            return jsonify({"error": "Values 'a' and 'b' must be numbers"}), 400
        
        # Perform calculations
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
        
        # Return successful response
        return jsonify({
            "operation": operation,
            "a": a,
            "b": b,
            "result": result
        })
        
    except Exception as e:
        # Log unexpected errors
        logger.error(f"Unexpected error in math endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)