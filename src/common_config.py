import os
from dotenv import load_dotenv 

load_dotenv()

MONGO_CONNECTION_STRING = os.environ.get("MONGO_CONNECTION_STRING", None)
DB_NAME = os.environ.get("DB_NAME", None)
ALLOWED_CORS_ORIGIN = os.environ.get("ALLOWED_CORS_ORIGIN", "").split(",")
PORT = os.environ.get("PORT", "8000")