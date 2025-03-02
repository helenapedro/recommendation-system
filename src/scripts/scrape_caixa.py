import requests
import warnings
import json
import os
import sys
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning  # Disable SSL warnings

# Add the parent directory to the system path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers.db_connection import db, client

warnings.simplefilter("ignore", InsecureRequestWarning)

# Access the "branches" collection
branches_collection = db["branches"]

# 🔹 Function to scrape CAIXA branches with coordinates
def scrape_caixa_agencies(url):
    print(f"🔍 Accessing {url} to collect data for CAIXA branches.")
    try:
        # Access the page
        response = requests.get(url, timeout=10, verify=False)
        if response.status_code != 200:
            print(f"❌ Error processing {url}: {response.status_code}")
            return

        # Parse the page
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract branch details
        branches = []
        seen_branches = set()
        branch_items = soup.find_all("div", class_="bank_agency_item")
        for item in branch_items:
            try:
               name = item.find("h4").text.strip()  # Branch name
               address = item.find("div", class_="info").text.strip()  # Address
               
               if (name, address) in seen_branches:
                   continue
               seen_branches.add((name, address))
                 
               province = item.find("h6").text.strip()  # Province
               address = item.find("div", class_="info").text.strip()  # Address
               phone_tag = item.find("a", href=lambda href: href and href.startswith("tel:"))
               phone = phone_tag.text.strip() if phone_tag else "N/A"
               opening_hours_tag = item.find("img", src="/images/clock.svg").find_next("div", class_="info")
               opening_hours = opening_hours_tag.text.strip() if opening_hours_tag else "N/A"

               branches.append({
                    "name": name,
                    "endereco": address,
                    "province": province,
                    "telefone": phone,
                    "horario_funcionamento": opening_hours
               })
            except Exception as e:
                print(f"⚠ Error extracting branch details: {e}")

        # Extract latitude and longitude from data-markers
        map_div = soup.find("div", class_="half-maps")
        if not map_div:
            print("❌ Could not find map data.")
            return

        # Parse the JSON data from `data-markers`
        data_markers = json.loads(map_div["data-markers"])
        coordinates = [
            {"latitude": marker["latitude"], "longitude": marker["longitude"]}
            for marker in data_markers
        ]

        # Check if branch count matches coordinate count
        if len(branches) != len(coordinates):
            print(f"⚠ Mismatch: {len(branches)} branches but {len(coordinates)} coordinates found!")
            return

        # Match branches with coordinates
        for idx, branch in enumerate(branches):
            try:
                coord = coordinates[idx]
                branch["latitude"] = coord["latitude"]
                branch["longitude"] = coord["longitude"]

                # Insert or update in MongoDB
                result = branches_collection.update_one(
                    {
                        "name": branch["name"],
                        "endereco": branch["endereco"],
                        "province": branch["province"]
                    },
                    {"$set": branch},
                    upsert=True
                )

                if result.matched_count > 0:
                    print(f"✅ Branch updated: {branch['name']}")
                elif result.upserted_id:
                    print(f"✅ Branch added: {branch['name']}")
            except Exception as e:
                print(f"⚠ Error while matching branch: {e}")

    except Exception as e:
        print(f"⚠ Error while processing {url}: {e}")


# 🔹 Scrape CAIXA branches
scrape_caixa_agencies("https://www.caixaangola.ao/institucional/rede-de-agencias")

# 🔹 Close the MongoDB connection
client.close()
