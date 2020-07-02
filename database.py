import json
import os
import re


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

    def search_term(cls, term, guild_id):
        response = {
            "success": False,
            "results": []
        }
        try:
            rgx = re.compile(f'.*{term}.*', re.IGNORECASE)
            search_result = cls.collection.find({ 'term': rgx, 'guild_id': guild_id },{ 'term':1 })
        except Exception as e:
            print(f"Exception occured while querying search history with  term {term} and guild ID {guild_id} as {e}")
        else:
            response['success'] = True
            response['results'] = list(search_result)
            print(f"Query Response is: {response['results']}")

        return response
