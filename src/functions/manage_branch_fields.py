import os
import sys

# Add the parent directory to the system path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from helpers.db_connection import db, client

# Access the "branches" collection
branches_collection = db["branches"]

def manage_branch_field(branch_filter, operation, field_name, field_value=None):
    """
    Function to add, delete, or update a field in a branch document.

    Parameters:
    - branch_filter: Dictionary to find the branch (e.g., {"_id": ObjectId("...")})
    - operation: "add", "delete", or "update"
    - field_name: The name of the field to modify
    - field_value: The value to set (for add/update)
    """
    try:
        if operation == "add" or operation == "update":
            # Add or update the field
            update_query = {"$set": {field_name: field_value}}
            result = branches_collection.update_one(branch_filter, update_query)
            if result.matched_count > 0:
                print(f"✅ Field '{field_name}' {'added' if operation == 'add' else 'updated'} successfully!")
            else:
                print(f"⚠ No branch matched the filter: {branch_filter}")

        elif operation == "delete":
            # Delete the field
            update_query = {"$unset": {field_name: ""}}
            result = branches_collection.update_one(branch_filter, update_query)
            if result.matched_count > 0:
                print(f"✅ Field '{field_name}' deleted successfully!")
            else:
                print(f"⚠ No branch matched the filter: {branch_filter}")
        else:
            print("⚠ Invalid operation. Use 'add', 'delete', or 'update'.")
    except Exception as e:
        print(f"⚠ Error occurred: {e}")

# Example Usage:

# 1. Add a field (e.g., adding a "manager" field with value "John Doe")
manage_branch_field(
    branch_filter={"name": "BCI Hoji Ya Henda"},  # Filter to match the branch
    operation="add",
    field_name="manager",
    field_value="John Doe"
)

# 2. Update a field (e.g., updating the "telefone" field)
manage_branch_field(
    branch_filter={"name": "BCI Hoji Ya Henda"},  # Filter to match the branch
    operation="update",
    field_name="telefone",
    field_value="+244 923 456 789"
)

# 3. Delete a field (e.g., removing the "latitude" field)
manage_branch_field(
    branch_filter={"name": "BCI Hoji Ya Henda"},  # Filter to match the branch
    operation="delete",
    field_name="latitude"
)

# Close the MongoDB connection
client.close()
