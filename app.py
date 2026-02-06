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

if __name__ == '__main__':
    app.run(debug=True)