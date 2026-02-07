"""Stock movement route handlers."""
from flask import Blueprint, request, jsonify

movement_bp = Blueprint("movement", __name__)


@movement_bp.route("/", methods=["GET"])
def list_movements():
    return jsonify({"movements": [], "message": "Movement listing endpoint"})

