import json
import os


from pymongo import MongoClient


MONGO_CONNECTION_URI = os.environ.get('MONGO_CONNECTION_URI')
if MONGO_CONNECTION_URI is None:
    env_config = json.loads(open('dev.json', 'r').read())
    MONGO_CONNECTION_URI = env_config.get('MONGO_CONNECTION_URI')


def singleton(cls):
    def wrapper(*args, **kwargs):
        if wrapper.instance is None:
            wrapper.instance = cls(*args, **kwargs)
        return wrapper.instance
    wrapper.instance = None
    return wrapper


@singleton
class DB:
    def __init__(cls):
        cls.client = MongoClient(MONGO_CONNECTION_URI)
        cls.collection = cls.client['primary']['searchhistory']
    
    def store(cls, **kwargs):
        try:
            store_result = cls.collection.insert_one(dict(kwargs))
        except Exception as e:
            print(f"Exception occured while storing search request data {dict(kwargs)} as {e}")
        else:
            print(f"Storing search request data successful with response: {store_result}")
