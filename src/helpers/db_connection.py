from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get MongoDB URI from .env
mongo_uri = os.getenv("RECOMMENDATION_DB_MONGO_URI")

# Create a MongoDB client and access the database
try:
    client = MongoClient(mongo_uri)
    print("Connected to MongoDB successfully!")
    
    db = client['recommendation-db']
    print("Database accessed successfully!")
    
except Exception as e:
    print(f"An error occurred: {e}")
