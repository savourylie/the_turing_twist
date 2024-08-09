from pymongo import MongoClient
from pydantic import BaseModel
from database.mongodb import MongoDB
from data_model.elo_score import EloScore


# Connect to MongoDB
dao = MongoDBDAO()

# client = MongoClient('mongodb://localhost:27017/')
# db = client['the_turing_twist']
# collection = db['elo_scores']

# Create an instance of EloScore
elo_score = EloScore(model_name="GPT-4o")

# # Convert Pydantic model to dictionary
# elo_score_dict = elo_score.model_dump()

# Insert into MongoDB
result = dao.insert(elo_score)

print(f"Inserted document ID: {result.inserted_id}")

# # Update operation
# model_name_to_update = "GPT-3"
# new_elo_score = 150

# update_result = collection.update_one(
#     {"model_name": model_name_to_update},
#     {"$set": {"elo_score": new_elo_score}}
# )

# if update_result.modified_count > 0:
#     print(f"Updated elo_score for {model_name_to_update}")
# else:
#     print(f"No document found with model_name: {model_name_to_update}")