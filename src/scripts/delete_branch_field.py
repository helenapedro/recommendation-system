from helpers.db_connection import db, client

# Access the "branches" collection
branches_collection = db["branches"]

try:
    # Define the filter to target documents with `bank_id = "BCI"` and an existing `id` field
    filter_query = {"bank_id": "BCI", "253079038_location": {"$exists": True}}

    # Define the update to unset (remove) the `id` field
    update_query = {"$unset": {"253079038_location": ""}}

    # Perform the update operation
    result = branches_collection.update_many(filter_query, update_query)

    # Print the result
    print(f"✅ Successfully deleted `253079038_location` field from {result.modified_count} branches with `bank_id = BCI`.")

except Exception as e:
    print(f"⚠ Error occurred while deleting `253079038_location` field: {e}")

finally:
    # Close the MongoDB connection
    client.close()
