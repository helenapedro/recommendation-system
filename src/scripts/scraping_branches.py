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

# 🔹 Find banks and its websites
banks = banks_collection.find({"website": {"$ne": ""}})

# 🔹 Funtion to collect branches info
def scrape_bank_agencies(bank):
    url = bank["website"]
    print(f"🔍 Accessing {url} to colect data from branches of {bank['nome']}")

    try:
        response = requests.get(url, timeout=10, verify=False)
        if response.status_code != 200:
            print(f"❌ Error processing {url}: {response.status_code}")
            return

        soup = BeautifulSoup(response.text, "html.parser")

        # Fetch branches list
        branches = soup.find_all("div", class_="b-container")
        
        for branch in branches:
          # Extract branch details
          name = branch.find("div", class_="b-title").text.strip()
          address = branch.find_all("div")[1].text.strip()  # Second <div> for the address
          province = branch.find_all("div")[2].text.strip()  # Third <div> for the province
          opening_hours = branch.find("div").find_next("p").text.strip()  # Opening hours
          
          # Create document for the database
          branch_data = {
               "bank_id": bank["_id"],
               "name": name,
               "endereco": address,
               "province": province,
               "latitude": None,
               "longitude": None,
               "horario_funcionamento": opening_hours,
               "servicos_disponiveis": [],  # If additional services are available
               "tempo_medio_espera": None,
               "avaliacoes": []
          }
    
          # Insert into MongoDB
          branches_collection.insert_one(branch_data)
          print(f"✅ Branch added: {name}")

    except Exception as e:
        print(f"⚠ Error while processing {url}: {e}")

# 🔹 Rodar o scraping para todos os bancos
for bank in banks:
    scrape_bank_agencies(bank)

# 🔹 Fechar conexão com MongoDB
client.close()