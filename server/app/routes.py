from app import app, limiter


@app.route("/", methods=["GET"])
@limiter.limit("5 per 5 second")
def index():
    return "healthy"
