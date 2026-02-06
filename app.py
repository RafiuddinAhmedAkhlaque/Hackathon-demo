"""
Flask application with hello endpoint
"""
from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/hello', methods=['GET'])
def hello():
    """Hello endpoint that returns a greeting message"""
    return jsonify({"message": "Hello, World!"})

@app.route('/goodbye', methods=['GET'])
def goodbye():
    """Goodbye endpoint that returns a farewell message"""
    return jsonify({"message": "Goodbye, World!"})

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint that returns system status"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "version": "1.0.0"
    })

if __name__ == '__main__':
    app.run(debug=True)