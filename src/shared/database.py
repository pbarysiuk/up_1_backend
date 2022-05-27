from pymongo import MongoClient
from os import environ


def get_connection():
    client = MongoClient(environ.get("MONGODB_CONNSTRING"))
    db = client.drugbank
    return db
