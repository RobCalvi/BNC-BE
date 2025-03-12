from app.db.database import MongoClient
import os

client = MongoClient(os.environ.get("MONGO_DB_NAME"))


def get_mongo_client():
    return client
