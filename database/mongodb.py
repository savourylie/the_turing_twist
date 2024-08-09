from pymongo import MongoClient
from data_model.elo_score import EloScore
from bson import ObjectId
from datetime import datetime
from icecream import ic

class MongoDB:
    def __init__(self, connection_string='mongodb://localhost:27017/'):
        self.client = MongoClient(connection_string)
        self.db = self.client['the_turing_twist']
        self.collection = self.db['elo_scores']

    def check_record_exists(self, model_name: str) -> bool:
        # Function to check if a record exists
        record = self.collection.find_one({"model_name": model_name})
        return record is not None

    def insert(self, elo_score: EloScore):
        # # Convert Pydantic model to dictionary
        elo_score_dict = elo_score.model_dump()
        ic(type(elo_score_dict), elo_score_dict)
        result = self.collection.insert_one(elo_score_dict)

        return result
    
    def find(self, query):
        return self.collection.find(query)
    
    def update(self, query, data):
        self.collection.update_one(query, data)
    
    def delete(self, query):
        self.collection.delete_one(query)


class EloScoreDAO:
    def __init__(self, mongodb: MongoDB):
        self.mongodb = mongodb
    
    def check_model_exists(self, model_name: str) -> bool:
        return self.mongodb.check_record_exists(model_name)
    
    def get_elo_score_for_model(self, model_name: str) -> dict:
        query = {"model_name": model_name}
        record = self.mongodb.collection.find_one(query)

        return record
    
    def update_elo_score(self, model_name: str, elo_score: EloScore):

        update_data = elo_score.model_dump()

        update_result = self.mongodb.collection.update_one(
            {"model_name": model_name},
            {"$set": update_data},
            upsert=True
        )

        return update_result.modified_count > 0 or update_result.upserted_id is not None