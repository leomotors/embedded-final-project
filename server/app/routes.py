from app import app, limiter


@app.route("/", methods=["GET"])
@limiter.limit("5 per 5 second")
def index():
    return "healthy"


@app.route("/golden-frame", methods=["POST"])
@limiter.limit("1 per 5 second")
def golden_frame():
    return "golden frame"

    # add golden_frame function here
