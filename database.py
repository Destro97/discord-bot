import json
import os
import re


from pymongo import MongoClient


### Load Mongo Connection String from environment on PROD
### Otherwise load it from local file
MONGO_CONNECTION_URI = os.environ.get('MONGO_CONNECTION_URI')
if MONGO_CONNECTION_URI is None:
    env_config = json.loads(open('dev.json', 'r').read())
    MONGO_CONNECTION_URI = env_config.get('MONGO_CONNECTION_URI')


### Decorator to only ever have a single instance of DB
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

        ### Initialise the MongoDB Client
        cls.client = MongoClient(MONGO_CONNECTION_URI)

        ### Initialise the Collection to use for storing data
        cls.collection = cls.client['primary']['searchhistory']


    def store(cls, **kwargs):
        """
        Method to store information in Database
        """

        try:
            ### Try inserting data inside DB as a single document
            store_result = cls.collection.insert_one(dict(kwargs))
        except Exception as e:
            ### Log the error in case insertion operation raised an Exception
            print(f"Exception occured while storing search request data {dict(kwargs)} as {e}")
        else:
            ### Log the response in case the insertion operation was successful
            print(f"Storing search request data successful with response: {store_result}")


    def search_term(cls, term, guild_id):
        """
        Method to fetch documents from database corresponding to
        specified Guild ID and Search Term
        term: Search Term based on which regex will be compiled to query
        guild_id: Guild ID to find results pertaining to that Guild only
        """

        ### Define response structure
        response = {
            "success": False,
            "results": []
        }

        try:
            ### Compiling regex to query for any documents containing the search term
            rgx = re.compile(f'.*{term}.*', re.IGNORECASE)

            ### Try to find documents from DB containing search term and provided Guild ID
            ### Only return 'term' from document for matching documents
            search_result = cls.collection.find({
                    'term': rgx,
                    'guild_id': guild_id
                },{
                    'term':1
                }
            )
        except Exception as e:
            ### Log the error in case query operation raised an Exception
            print(f"Exception occured while querying search history with term {term} and guild ID {guild_id} as {e}")
        else:
            ### Prepare response dict in case query operation was successful
            response['success'] = True
            response['results'] = list(search_result)
            print(f"Query Response is: {response['results']}")

        return response
