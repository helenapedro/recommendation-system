import requests
from bs4 import BeautifulSoup
import json
import os
import sys

# Add the parent directory to the system path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from helpers.db_connection import db, client

try:
    # Access the collection
    branches_collection = db['branches']

    # Target bank URL
    url = "https://www.bancobai.ao/pt/pontos/agencias"
    response = requests.get(url, timeout=10, verify=False)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find the <script> tag containing `viewBagBranchesList`
        script_tag = soup.find("script", string=lambda s: s and "viewBagBranchesList" in s)

        if script_tag:
            # Extract the JavaScript content
            script_content = script_tag.string.strip()
            
            # Locate the JSON data
            json_start = script_content.find("viewBagBranchesList = ") + len("viewBagBranchesList = ")
            json_end = script_content.find("];", json_start) + 1
            json_data = script_content[json_start:json_end]
            
            # Parse the JSON data
            branches = json.loads(json_data)

            # Process each branch in the JSON data
            for branch in branches:
                try:
                    # Extract branch details
                    name = branch.get("Name", "N/A").strip()
                    address = branch.get("Address", "N/A").strip()
                    province = branch.get("Province", "N/A").strip()
                    phone = branch.get("Telephone", "N/A").strip()
                    latitude = branch.get("Latitude", None)
                    longitude = branch.get("Longitude", None)
                    schedule = branch.get("Schedule", "N/A").strip()

                    # Update or insert the branch in the database
                    result = branches_collection.update_one(
                        {"name": name, "endereco": address, "province": province},  # Match on these fields
                        {"$set": {
                            "bank_id": "BAI",
                            "telefone": phone,
                            "latitude": latitude,
                            "longitude": longitude,
                            "horario_funcionamento": schedule,
                            "servicos_disponiveis": [],
                            "tempo_medio_espera": None,
                            "avaliacoes": []
                        }},
                        upsert=True  # Insert if it doesn't exist
                    )

                    if result.matched_count > 0:
                        print(f"✅ Branch updated: {name}")
                    elif result.upserted_id:
                        print(f"✅ Branch added: {name}")
                    else:
                        print(f"⚠ No changes made for branch: {name}")

                except Exception as branch_error:
                    print(f"⚠ Error while processing branch: {branch_error}")
        else:
            print("❌ Could not find the script containing 'viewBagBranchesList'.")

except Exception as e:
    print(f"⚠ Error occurred: {e}")

finally:
    # Close the MongoDB connection
    client.close()
