"""Inventory Service - Main Application Entry Point"""
import json
import logging
import time
from datetime import datetime, timezone
from flask import Flask, g, request
from routes.stock_routes import stock_bp
from routes.warehouse_routes import warehouse_bp
from routes.movement_routes import movement_bp

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__)

    app.register_blueprint(stock_bp, url_prefix="/stock")
    app.register_blueprint(warehouse_bp, url_prefix="/warehouses")
    app.register_blueprint(movement_bp, url_prefix="/movements")

    @app.before_request
    def before_request():
        g.start_time = time.time()

    @app.after_request
    def after_request(response):
        duration_ms = round((time.time() - g.start_time) * 1000, 2)
        
        log_data = {
            "method": request.method,
            "path": request.path,
            "status": response.status_code,
            "duration_ms": duration_ms,
            "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        }
        
        logger.info(json.dumps(log_data))
        return response

    @app.route("/health")
    def health():
        return {"status": "healthy", "service": "inventory-service"}

    @app.route("/hello")
    def hello():
        return {"message": "hello"}

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8005)

