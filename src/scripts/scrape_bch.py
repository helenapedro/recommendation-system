import requests
import warnings
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

# 🔹 Function to scrape BCH branches
def scrape_bch_agencies(url):
    print(f"🔍 Accessing {url} to collect data for BCH branches.")
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
        branch_items = soup.find_all("div", class_="addresses-list--item")
        for item in branch_items:
            try:
                name = item.find("div", class_="addresses-list--item-title").text.strip()  # Branch name
                province = item.find("div", class_="addresses-list--item-location").text.strip()  # Province
                address = item.find("div", class_="addresses-list--item-contact").text.strip()  # Address

                # Extract phone numbers
                phone_numbers = []
                phone_items = item.find_all("div", class_="addresses-list--item-contact-phone")
                for phone_item in phone_items:
                    phone_text = phone_item.find("span", class_="col-xs-9").text.strip()
                    if phone_text and phone_text != ".":
                        phone_numbers.append(phone_text)

                branches.append({
                    "name": name,
                    "endereco": address,
                    "province": province,
                    "telefone": phone_numbers,  # List of phone numbers
                    "latitude": None,  # Placeholder for latitude
                    "longitude": None,  # Placeholder for longitude
                    "horario_funcionamento": None,  # Placeholder for working hours
                    "servicos_disponiveis": [],
                    "tempo_medio_espera": None,
                    "avaliacoes": []
                })
            except Exception as e:
                print(f"⚠ Error extracting branch details: {e}")

        # Insert or update branches in MongoDB
        for branch in branches:
            try:
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
                print(f"⚠ Error inserting branch into database: {e}")

    except Exception as e:
        print(f"⚠ Error while processing {url}: {e}")


# 🔹 Scrape BCH branches
scrape_bch_agencies("https://www.bch.co.ao/inicio/onde-estamos")

# 🔹 Close the MongoDB connection
client.close()
