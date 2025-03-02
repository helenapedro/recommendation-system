import os
import sys

# Add the parent directory to the system path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from helpers.db_connection import db

#print(client.list_database_names())

#db = client['recommendation_db']
#print(db.list_collection_names())

try:
    # Access the database and collection
    collection = db['banks']

    # Data to insert
    banks = [
        {"_id": "ATL", "nome": "BANCO MILLENNIUM ATLÂNTICO, S.A.", "numero_registro": 55, "website": ""},
        {"_id": "BAI", "nome": "BANCO ANGOLANO DE INVESTIMENTOS, S.A.", "numero_registro": 40, "website": ""},
        {"_id": "BCA", "nome": "BANCO COMERCIAL ANGOLANO, S.A.", "numero_registro": 43, "website": ""},
        {"_id": "BCGA", "nome": "BANCO CAIXA GERAL ANGOLA, S.A.", "numero_registro": 4, "website": ""},
        {"_id": "BCH", "nome": "BANCO COMERCIAL DO HUAMBO, S.A.", "numero_registro": 59, "website": ""},
        {"_id": "BCI", "nome": "BANCO DE COMÉRCIO E INDÚSTRIA, S.A.", "numero_registro": 5, "website": ""},
        {"_id": "BCS", "nome": "BCS – BANCO DE CRÉDITO DO SUL, S.A.", "numero_registro": 70, "website": ""},
        {"_id": "BDA", "nome": "BANCO DE DESENVOLVIMENTO DE ANGOLA, S.A.", "numero_registro": 54, "website": ""},
        {"_id": "BE", "nome": "BANCO ECONÓMICO, S.A.", "numero_registro": 45, "website": ""},
        {"_id": "BFA", "nome": "BANCO DE FOMENTO ANGOLA, S.A.", "numero_registro": 6, "website": ""},
        {"_id": "BIC", "nome": "BANCO BIC, S.A.", "numero_registro": 51, "website": ""},
        {"_id": "BIR", "nome": "BANCO DE INVESTIMENTO RURAL, S.A.", "numero_registro": 67, "website": ""},
        {"_id": "BNI", "nome": "BANCO DE NEGÓCIOS INTERNACIONAL, S.A.", "numero_registro": 52, "website": ""},
        {"_id": "BOCLB", "nome": "BANCO DA CHINA LIMITADA – SUCURSAL EM LUANDA", "numero_registro": 71, "website": ""},
        {"_id": "BPC", "nome": "BANCO DE POUPANÇA E CRÉDITO, S.A.", "numero_registro": 10, "website": ""},
        {"_id": "BSOL", "nome": "BANCO SOL, S.A.", "numero_registro": 44, "website": ""},
        {"_id": "BVB", "nome": "BANCO VALOR, S.A.", "numero_registro": 62, "website": ""},
        {"_id": "FNB", "nome": "FINIBANCO ANGOLA, S.A.", "numero_registro": 58, "website": ""},
        {"_id": "BKEVE", "nome": "BANCO KEVE, S.A.", "numero_registro": 47, "website": ""},
        {"_id": "SBA", "nome": "STANDARD BANK DE ANGOLA, S.A.", "numero_registro": 60, "website": ""},
        {"_id": "SCBA", "nome": "STANDARD CHARTERED BANK DE ANGOLA, S.A.", "numero_registro": 63, "website": ""},
        {"_id": "VTB", "nome": "BANCO VTB ÁFRICA, S.A.", "numero_registro": 56, "website": ""},
        {"_id": "YETU", "nome": "BANCO YETU, S.A.", "numero_registro": 66, "website": ""}
    ]

    # Insert data into the collection
    result = collection.insert_many(banks)
    print(f"Inserted {len(result.inserted_ids)} records successfully!")

except Exception as e:
    print(f"An error occurred: {e}")
