"""
Flask application with hello endpoint
"""
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/hello', methods=['GET'])
def hello():
    """Hello endpoint that returns a greeting message"""
    return jsonify({"message": "Hello, World!"})

if __name__ == '__main__':
    app.run(debug=True)