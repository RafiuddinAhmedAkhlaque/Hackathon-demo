"""
Flask application with hello endpoint
"""
import logging
import time
from datetime import datetime, timezone
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

@app.route('/echo', methods=['POST'])
def echo():
    """Echo endpoint that returns the input message with metadata"""
    try:
        # Check if request contains JSON
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400
        
        data = request.get_json()
        
        # Check if 'message' field is present
        if data is None or 'message' not in data:
            return jsonify({"error": "Missing 'message' field in request body"}), 400
        
        message = data['message']
        
        # Handle the case where message is not a string
        if not isinstance(message, str):
            return jsonify({"error": "'message' field must be a string"}), 400
        
        # Calculate metadata
        character_count = len(message)
        word_count = len(message.split()) if message.strip() else 0
        reversed_message = message[::-1]
        uppercase_message = message.upper()
        timestamp = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        
        # Return response with metadata
        response = {
            "original_message": message,
            "character_count": character_count,
            "word_count": word_count,
            "reversed": reversed_message,
            "uppercase": uppercase_message,
            "timestamp": timestamp
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error processing echo request: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)