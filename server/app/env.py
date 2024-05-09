import os

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
PORT = os.getenv("PORT")
ENV = os.getenv("ENV")


def is_dev():
    return ENV == "development"
