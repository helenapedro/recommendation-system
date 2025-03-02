from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# MongoDB connection
mongo_uri = os.getenv("RECOMMENDATION_DB_MONGO_URI")  
client = MongoClient(mongo_uri)

try:
    # Access the database and collection
    db = client['recommendation-db']
    collection = db['banks']
    
    # Update data in the collection
    result = collection.update_one({"_id": "ATL"}, {"$set": {"website": "http://www.atlantico.ao/"}})
    print(f"Updated {result.modified_count} record successfully!")

except Exception as e:
    print(f"An error occurred: {e}")
