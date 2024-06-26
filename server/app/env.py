import os

from app import logging
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
PORT = os.getenv("PORT")
ENV = os.getenv("ENV")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DISCORD_CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")
CAPTION_MESSAGE = os.getenv("CAPTION_MESSAGE")

if API_KEY is None or len(API_KEY) < 6:
    logging.warn("API_KEY is not set or is too short")


def is_dev():
    return ENV == "development"
