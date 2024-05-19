from app import app
from env import API_KEY
from flask import abort, request


@app.before_request
def auth():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        abort(401, "Authorization header is missing")

    _, key = auth_header.split(" ", 1)
    if key != API_KEY:
        abort(403, "Invalid API key")
