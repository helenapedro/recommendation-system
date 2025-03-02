from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get MongoDB URI from .env
mongo_uri = os.getenv("MONGO_URI")

# Create a MongoDB client
try:
    client = MongoClient(mongo_uri)
    print("Connected to MongoDB successfully!")
    
    # Access a specific database and collection
    db = client['recommendation_db']
    print("Database accessed successfully!")
except Exception as e:
    print(f"An error occurred: {e}")
