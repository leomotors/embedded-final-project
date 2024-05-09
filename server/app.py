import logging

from flask import Flask, jsonify, request
from flask_cors import CORS
from waitress import serve

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)


@app.route("/")
def index():
    return "healthy"


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8080)
