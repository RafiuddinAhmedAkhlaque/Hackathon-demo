"""
Flask application with hello endpoint
"""
import logging
import time
from datetime import datetime
from flask import Flask, jsonify, request, g

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

def generate_timestamp():
    """
    Generate ISO 8601 formatted timestamp in UTC
    
    Returns:
        str: ISO 8601 formatted timestamp (e.g., "2026-02-06T12:30:00Z")
    """
    return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

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
    return jsonify({
        "message": "Hello, World!",
        "timestamp": generate_timestamp()
    })

@app.route('/goodbye', methods=['GET'])
def goodbye():
    """Goodbye endpoint that returns a farewell message"""
    return jsonify({
        "message": "Goodbye, World!",
        "timestamp": generate_timestamp()
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": generate_timestamp()
    })

if __name__ == '__main__':
    app.run(debug=True)