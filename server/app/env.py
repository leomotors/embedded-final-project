import os

from app import logging
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
PORT = os.getenv("PORT")
ENV = os.getenv("ENV")

if API_KEY is None or len(API_KEY) < 6:
    logging.warn("API_KEY is not set or is too short")


def is_dev():
    return ENV == "development"
