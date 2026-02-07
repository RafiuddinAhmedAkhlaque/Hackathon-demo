"""Simple Flask API with greeting endpoints"""
from flask import Flask, jsonify
import re


def create_app():
    app = Flask(__name__)

    @app.route("/hello")
    def hello():
        """Generic hello endpoint"""
        return jsonify({"message": "Hello, World!"})

    @app.route("/hello/<name>")
    def hello_name(name):
        """Personalized hello endpoint"""
        # Validate name - should not be empty or contain numbers
        if not name or not name.strip():
            return jsonify({
                "error": "Name cannot be empty",
                "message": "Please provide a valid name"
            }), 400
        
        # Check for numbers in the name
        if re.search(r'\d', name):
            return jsonify({
                "error": "Name cannot contain numbers",
                "message": "Please provide a name without numbers"
            }), 400
        
        return jsonify({"message": f"Hello, {name}!"})

    @app.route("/health")
    def health():
        """Health check endpoint"""
        return jsonify({"status": "healthy", "service": "greeting-api"})

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8000, debug=True)