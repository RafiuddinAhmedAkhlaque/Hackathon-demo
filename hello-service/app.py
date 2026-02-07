"""Hello Service - Main Application Entry Point"""
import re
from flask import Flask, jsonify


def create_app():
    app = Flask(__name__)

    @app.route("/hello")
    def hello():
        """Generic hello endpoint that returns Hello, World!"""
        return jsonify({"message": "Hello, World!"})

    @app.route("/hello/<name>")
    def hello_name(name):
        """Personalized hello endpoint that accepts a name parameter"""
        # Check if name is empty or contains numbers
        if not name or not name.strip():
            return jsonify({"error": "Name cannot be empty"}), 400
        
        # Check if name contains numbers
        if re.search(r'\d', name):
            return jsonify({"error": "Name cannot contain numbers"}), 400
        
        return jsonify({"message": f"Hello, {name}!"})

    @app.route("/health")
    def health():
        return {"status": "healthy", "service": "hello-service"}

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8006)