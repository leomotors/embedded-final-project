import logging

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)


@app.route("/")
def index():
    return "healthy"
