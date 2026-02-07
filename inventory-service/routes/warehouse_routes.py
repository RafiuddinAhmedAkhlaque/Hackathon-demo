"""Warehouse route handlers."""
from flask import Blueprint, request, jsonify

warehouse_bp = Blueprint("warehouse", __name__)


@warehouse_bp.route("/", methods=["GET"])
def list_warehouses():
    return jsonify({"warehouses": [], "message": "Warehouse listing endpoint"})


@warehouse_bp.route("/<warehouse_id>", methods=["GET"])
def get_warehouse(warehouse_id):
    return jsonify({"warehouse_id": warehouse_id, "message": "Warehouse detail endpoint"})

