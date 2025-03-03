import json
import os
import sys

# Add the parent directory to the system path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the db and client from db_connection.py
from helpers.db_connection import db, client

# Access the BCI branches collection
branches_collection = db['branches']

# Load the JSON data from the file
with open('C:/Users/mbeua/Área de Trabalho/Projects/Current/recommendation-system/src/playground.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Function to dynamically extract and insert data into the branches collection
def extract_and_insert(data):
    for item in data:
        if 'features' in item:
            for feature in item['features']:
                if 'c' in feature:
                    try:
                        # Parse the JSON object stored in the 'c' field
                        c_data = json.loads(feature['c'])

                        # Dynamically build the document
                        document = {
                            "bank_id": "BCI",  # Associate the branch with BCI
                            "id": feature['id'],  # Unique feature ID
                        }

                        # Add all top-level keys from 'c' dynamically
                        for key, value in c_data.items():
                            # Handle nested objects if needed
                            if isinstance(value, dict):
                                for nested_key, nested_value in value.items():
                                    document[f"{key}_{nested_key}"] = nested_value
                            else:
                                document[key] = value

                        # Insert or update the document in MongoDB
                        result = branches_collection.update_one(
                            {"id": document["id"]},  # Match based on the unique branch 'id'
                            {"$set": document},     # Update document if it exists, or insert if new
                            upsert=True
                        )

                        if result.matched_count > 0:
                            print(f"✅ Branch updated: {document.get('endereco', 'Unnamed')}")
                        elif result.upserted_id:
                            print(f"✅ Branch added: {document.get('endereco', 'Unnamed')}")
                    except Exception as e:
                        print(f"⚠ Error processing feature {feature['id']}: {e}")

# Call the function to extract and insert data
extract_and_insert(data)

# Close the MongoDB connection
client.close()
