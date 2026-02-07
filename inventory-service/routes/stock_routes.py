"""Stock route handlers."""
from flask import Blueprint, request, jsonify

stock_bp = Blueprint("stock", __name__)


@stock_bp.route("/", methods=["GET"])
def list_stock():
    return jsonify({"items": [], "message": "Stock listing endpoint"})


@stock_bp.route("/<item_id>", methods=["GET"])
def get_stock(item_id):
    return jsonify({"item_id": item_id, "message": "Stock item endpoint"})

