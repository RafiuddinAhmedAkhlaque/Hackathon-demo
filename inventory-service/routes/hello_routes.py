"""Hello route handlers."""
import re
from flask import Blueprint, jsonify

hello_bp = Blueprint("hello", __name__)


@hello_bp.route("/", methods=["GET"])
def hello():
    """Generic hello endpoint."""
    return jsonify({"message": "Hello, World!"})


@hello_bp.route("/<name>", methods=["GET"])
def hello_personalized(name):
    """Personalized hello endpoint."""
    # Check if name is empty or contains numbers
    if not name or not name.strip():
        return jsonify({
            "error": "Name cannot be empty"
        }), 400
    
    if re.search(r'\d', name):
        return jsonify({
            "error": "Name cannot contain numbers"
        }), 400
    
    return jsonify({"message": f"Hello, {name}!"})