"""Inventory Service - Main Application Entry Point"""
from flask import Flask
from routes.stock_routes import stock_bp
from routes.warehouse_routes import warehouse_bp
from routes.movement_routes import movement_bp
from routes.hello_routes import hello_bp


def create_app():
    app = Flask(__name__)

    app.register_blueprint(stock_bp, url_prefix="/stock")
    app.register_blueprint(warehouse_bp, url_prefix="/warehouses")
    app.register_blueprint(movement_bp, url_prefix="/movements")
    app.register_blueprint(hello_bp, url_prefix="/hello")

    @app.route("/health")
    def health():
        return {"status": "healthy", "service": "inventory-service"}

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8005)

