import os

from waitress import serve

from server.app.app import app, logging
from server.app.env import PORT, is_dev

if is_dev():
    app.run(host="0.0.0.0", port=PORT, debug=True)
else:
    logging.info(f"Starting production server on port {PORT}")
    serve(app, host="0.0.0.0", port=PORT)
