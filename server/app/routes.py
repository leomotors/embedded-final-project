import io

import cv2
import numpy as np
from app import app, limiter
from discord import send_discord_message
from env import CAPTION_MESSAGE, DISCORD_BOT_TOKEN, DISCORD_CHANNEL_ID
from flask import Response, request
from lib import build_golden_frame, frames_info


@app.route("/", methods=["GET"])
@limiter.limit("5 per 5 second")
def index():
    return "healthy"


ALLOWED_FILE_TYPES = set(["image/jpeg", "image/png", "image/webp", "image/avif"])


@app.route("/golden-frame", methods=["POST"])
@limiter.limit("1 per 5 second")
def golden_frame():
    if "file" not in request.files:
        return "No file uploaded", 400

    file = request.files["file"]

    if not file or file.filename == "":
        return "No file selected", 400

    filetype = file.content_type
    if filetype not in ALLOWED_FILE_TYPES:
        return "Invalid file type", 400

    # * Get frame name
    frame_name = request.form.get("frame_name")

    if frame_name is None:
        return "No frame name selected", 400

    if not any(map(lambda x: x.name == frame_name, frames_info)):
        return "Invalid frame name", 400

    # * Get resolution option
    resolution = request.form.get("resolution") or 0
    try:
        res_int = int(resolution)
    except ValueError:
        return "Invalid resolution", 400

    if res_int < -5:
        return "Resolution multipler too big, must not exceed x5", 400

    if 0 < res_int < 360:
        return "Resolution too small, must be at least 360", 400

    if res_int > 4000:
        return "Resolution too big, must not exceed 4000", 400

    # * Get No Crop options
    nocrop = request.form.get("nocrop")
    crop = nocrop is None or len(nocrop) < 1

    # Read the image file as bytes
    image_bytes = file.read()

    # Convert the image bytes to a NumPy array
    nparr = np.frombuffer(image_bytes, np.uint8)

    # Decode the NumPy array into an OpenCV image
    input_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if input_image is None:
        return "Unable to parse input image", 400

    # Run the command
    out_image = build_golden_frame(frame_name, input_image, res_int, crop)

    # Create a response stream
    response_stream = io.BytesIO()

    ret, encoded_img = cv2.imencode(".png", out_image)
    response_stream.write(encoded_img.tobytes())

    # Set the appropriate headers for the response
    headers = {
        "Content-Disposition": f"attachment; filename=${file.filename}.out.png",
        "Content-Type": "image/png",
    }

    # Send discord request
    send_discord_message(
        DISCORD_BOT_TOKEN,
        DISCORD_CHANNEL_ID,
        response_stream.getvalue(),
        CAPTION_MESSAGE,
    )

    # Return the response with the image stream
    return Response(response_stream.getvalue(), headers=headers)
