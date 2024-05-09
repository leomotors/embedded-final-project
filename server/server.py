import os

from app import app, logging
from env import PORT, is_dev
from waitress import serve

if is_dev():
    logging.info(f"Starting dev server on port {PORT}")
    app.run(host="0.0.0.0", port=PORT, debug=True)
else:
    logging.info(f"Starting production server on port {PORT}")
    serve(app, host="0.0.0.0", port=PORT)
