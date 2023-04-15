import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_USER = os.environ.get("MONGODB_USERNAME", "")
MONGO_PASSWORD = os.environ.get("MONGODB_PASSWORD", "")
MONGO_CLUSTER_URL = os.environ.get("MONGODB_CLUSTER_URL", "")
MONGO_AUTH = "DEFAULT"

MONGODB_URI = f"mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_CLUSTER_URL}/?authMechanism={MONGO_AUTH}"

client = MongoClient(MONGODB_URI)
db = client["mydatabase"]

electricity_collection = db["electricity"]
accumulated_monthly = db["accumulated_monthly"]
