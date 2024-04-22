from pymongo import MongoClient
from pymongo.errors import (
    ConnectionFailure,
    DuplicateKeyError,
)
from src.common_config import MONGO_CONNECTION_STRING, DB_NAME

# validation needs to be done at application level before performing CRUD operations.
class WhizzyQuizMongoClient:
    def __init__(self, connection_string, db_name):
        self.MONGO_CONNECTION_STRING = connection_string
        self.DB_NAME = db_name
        self.client = None

    def connect(self):
        try:
            # print("MONGO_CONNECTION_STRING, DB_NAME: ", MONGO_CONNECTION_STRING, DB_NAME)
            if not self.MONGO_CONNECTION_STRING or not self.DB_NAME:
                raise ValueError("MONGO_CONNECTION_STRING or DB_NAME env cannot be empty.")

            self.client = MongoClient(self.MONGO_CONNECTION_STRING)
            self.db = self.client[self.DB_NAME]

        except ConnectionFailure as e:
            raise ConnectionFailure("Failed to connect to MongoDB: {}".format(e))
        except Exception as e:
            raise Exception("Error connecting to MongoDB: {}".format(e))

    def close(self):
        try:
            if self.client:
                self.client.close()
                self.client = None
                self.db = None
        except Exception as e:
            raise Exception("Error closing MongoDB connection: {}".format(e))
   
    # we can always add more params like sort, limit etc.
    def find(self, collection_name, query, projection={"_id": False}):
        try:
            col = self.db[collection_name]
            result = col.find(filter=query, projection=projection)

            return list(result)

        except Exception as e:
            raise KeyError("Something went wrong: {}".format(e))
        
    def aggregate(self, collection_name, pipeline, projection={"_id": False}):
        try:
            col = self.db[collection_name]
            pipeline.append({"$project": projection})
            result = col.aggregate(pipeline)
            return list(result)

        except Exception as e:
            raise KeyError("Error during aggregation: {}".format(e))

    def bulk_insert(self, collection_name, data):
        try:
            col = self.db[collection_name]
            col.insert_many(data)

            return "Successfully inserted Data"

        except DuplicateKeyError as e:
            raise KeyError("Duplicate key error: {}".format(e))  # Handle duplicate key error
        except ConnectionFailure as e:
            raise ConnectionFailure("Connection failure: {}".format(e))  # Handle connection failure
        except Exception as e:
            raise Exception("Error inserting data: {}".format(e))  # Handle other exceptions
        

wq_mongo_db_client = WhizzyQuizMongoClient(MONGO_CONNECTION_STRING, DB_NAME)
