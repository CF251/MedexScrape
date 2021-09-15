from pymongo import MongoClient


def get_mongo_connection():
    client = MongoClient()
    return client.vault
