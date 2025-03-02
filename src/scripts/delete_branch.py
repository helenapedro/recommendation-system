import os
import sys

# Add the parent directory to the system path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from helpers.db_connection import db, client

try:
    # Access the collection
    branches_collection = db['branches']

    # Define the deletion filter
    filter_query = {
        "bank_id": "BAI", 
        "latitude": None, 
        "longitude": None
    }

    # Perform the deletion
    result = branches_collection.delete_many(filter_query)

    # Print the result
    print(f"✅ Successfully deleted {result.deleted_count} branches where bank_id='BAI' and latitude/longitude=null.")

except Exception as e:
    print(f"⚠ Error occurred: {e}")

finally:
    # Close the MongoDB connection
    client.close()
