from pymongo import MongoClient


def get_connection():
    client = MongoClient("mongodb://AzureDiamondUsername:hrj3289d2pbIQ)9N@mongodb")
    db = client.drugbank
    return db
