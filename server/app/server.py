import middlewares
import routes
from app import app, logging
from env import PORT, is_dev
from waitress import serve

if is_dev():
    app.run(host="0.0.0.0", port=PORT, debug=True)
else:
    logging.info(f"Starting production server on port {PORT}")
    serve(app, host="0.0.0.0", port=PORT)
