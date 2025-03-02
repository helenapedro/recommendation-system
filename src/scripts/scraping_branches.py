import requests
import warnings
import os
import sys

# Add the parent directory to the system path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from helpers.db_connection import db, client
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning # Disable SSL warnings  

warnings.simplefilter('ignore', InsecureRequestWarning)

# Access the "banks" and "branches" collections
banks_collection = db["banks"]
branches_collection = db["branches"]

# 🔹 Find banks and their websites
banks = banks_collection.find({"website": {"$ne": ""}})

# 🔹 Function to collect branches info
def scrape_bank_agencies(bank):
    url = bank["website"]
    print(f"🔍 Accessing {url} to collect data from branches of {bank['nome']}")

    try:
        # Access the page
        response = requests.get(url, timeout=10, verify=False)
        if response.status_code != 200:
            print(f"❌ Error processing {url}: {response.status_code}")
            return

        # Parse the page
        soup = BeautifulSoup(response.text, "html.parser")

        # Fetch branches based on the bank's structure
        if bank["_id"] == "ATL":
            branches = soup.find_all("div", class_="b-container")
            for branch in branches:
                try:
                    # Extract branch details for ATL
                    name = branch.find("div", class_="b-title").text.strip()
                    address = branch.find_all("div")[1].text.strip()
                    province = branch.find_all("div")[2].text.strip()
                    opening_hours = branch.find("div").find_next("p").text.strip()

                    # Create branch data
                    branch_data = {
                        "bank_id": bank["_id"],
                        "name": name,
                        "endereco": address,
                        "province": province,
                        "telefone": None,
                        "latitude": None,
                        "longitude": None,
                        "horario_funcionamento": opening_hours,
                        "servicos_disponiveis": [],
                        "tempo_medio_espera": None,
                        "avaliacoes": []
                    }

                    # Insert or update in MongoDB
                    result = branches_collection.update_one(
                        {"name": name, "endereco": address, "province": province},
                        {"$set": branch_data},
                        upsert=True
                    )

                    if result.matched_count > 0:
                        print(f"✅ Branch updated: {name}")
                    elif result.upserted_id:
                        print(f"✅ Branch added: {name}")
                except Exception as branch_error:
                    print(f"⚠ Error while processing branch: {branch_error}")

        elif bank["_id"] == "BAI":
            branches = soup.find_all("div", class_="branches-list--row--branch")
            for branch in branches:
                try:
                    # Extract branch details for BAI
                    name = branch.find("div", class_="branches-list--row--branch--name").text.strip()
                    address = branch.find("div", class_="branches-list--row--branch--address").text.strip()
                    province = branch.find("div", class_="branches-list--row--branch--province").text.strip()
                    phone_tag = branch.find("div", class_="branches-list--row--branch--phone").find("a")
                    phone = phone_tag.text.strip() if phone_tag else "N/A"
                    latitude = None  # Placeholder for missing geolocation
                    longitude = None  # Placeholder for missing geolocation

                    # Create branch data
                    branch_data = {
                        "bank_id": bank["_id"],
                        "name": name,
                        "endereco": address,
                        "province": province,
                        "telefone": phone,
                        "latitude": latitude,
                        "longitude": longitude,
                        "horario_funcionamento": None,
                        "servicos_disponiveis": [],
                        "tempo_medio_espera": None,
                        "avaliacoes": []
                    }

                    # Insert or update in MongoDB
                    result = branches_collection.update_one(
                        {"name": name, "endereco": address, "province": province},
                        {"$set": branch_data},
                        upsert=True
                    )

                    if result.matched_count > 0:
                        print(f"✅ Branch updated: {name}")
                    elif result.upserted_id:
                        print(f"✅ Branch added: {name}")
                except Exception as branch_error:
                    print(f"⚠ Error while processing branch: {branch_error}")

        elif bank["_id"] == "CAIXA":
            branches = soup.find_all("div", class_="bank_agency_item")
            for branch in branches:
                try:
                    # Extract branch details for CAIXA
                    province = branch.find("h6").text.strip()  # Province
                    name = branch.find("h4").text.strip()  # Branch name
                    address = branch.find("div", class_="line").find_next("div", class_="info").text.strip()
                    phone_tag = branch.find("a", href=lambda href: href and href.startswith("tel:"))
                    phone = phone_tag.text.strip() if phone_tag else "N/A"
                    opening_hours_tag = branch.find("img", src="/images/clock.svg").find_next("div", class_="info")
                    opening_hours = opening_hours_tag.text.strip() if opening_hours_tag else "N/A"

                    # Create branch data
                    branch_data = {
                        "bank_id": bank["_id"],
                        "name": name,
                        "endereco": address,
                        "province": province,
                        "telefone": phone,
                        "latitude": None,
                        "longitude": None,
                        "horario_funcionamento": opening_hours,
                        "servicos_disponiveis": [],
                        "tempo_medio_espera": None,
                        "avaliacoes": []
                    }

                    # Insert or update in MongoDB
                    result = branches_collection.update_one(
                        {"name": name, "endereco": address, "province": province},
                        {"$set": branch_data},
                        upsert=True
                    )

                    if result.matched_count > 0:
                        print(f"✅ Branch updated: {name}")
                    elif result.upserted_id:
                        print(f"✅ Branch added: {name}")
                except Exception as branch_error:
                    print(f"⚠ Error while processing branch: {branch_error}")

        else:
            print(f"❌ Unsupported bank structure for {bank['nome']}")

    except Exception as e:
        print(f"⚠ Error while processing {url}: {e}")


# 🔹 Scrape branches for all banks
for bank in banks:
    scrape_bank_agencies(bank)

# 🔹 Close the MongoDB connection
client.close()
