"""Inventory Service - Main Application Entry Point"""
from flask import Flask, jsonify
import re
from routes.stock_routes import stock_bp
from routes.warehouse_routes import warehouse_bp
from routes.movement_routes import movement_bp


def create_app():
    app = Flask(__name__)

    app.register_blueprint(stock_bp, url_prefix="/stock")
    app.register_blueprint(warehouse_bp, url_prefix="/warehouses")
    app.register_blueprint(movement_bp, url_prefix="/movements")

    @app.route("/health")
    def health():
        return {"status": "healthy", "service": "inventory-service"}

    @app.route("/hello")
    def hello():
        return {"message": "Hello, World!"}

    @app.route("/hello/<name>")
    def hello_name(name):
        # Check if name is empty or contains numbers
        if not name or not name.strip():
            return jsonify({"error": "Name cannot be empty"}), 400
        
        if re.search(r'\d', name):
            return jsonify({"error": "Name cannot contain numbers"}), 400
        
        return {"message": f"Hello, {name}!"}

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8005)

