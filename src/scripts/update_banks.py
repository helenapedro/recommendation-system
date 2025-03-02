import os
import sys

# Add the parent directory to the system path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from helpers.db_connection import db

try:
    collection = db['banks']
    print("Collection accessed successfully!")
    
    updates = [
        {"_id": "ATL", "website": "https://www.atlantico.ao/pt/institucional/onde-estamos"},
        {"_id": "BAI", "website": "https://www.bancobai.ao/pt/pontos/agencias"},
        {"_id": "BCA", "website": ""},
        {"_id": "BCGA", "website": "https://www.caixaangola.ao/institucional/rede-de-agencias"},
        {"_id": "BCH", "website": "https://www.bch.co.ao/inicio/onde-estamos"},
        {"_id": "BCI", "website": "https://www.bci.ao/particular/contactos"},
        {"_id": "BCS", "website": "https://www.bancobcs.ao/quem-somos/o-banco/onde-estamos"},
        {"_id": "BDA", "website": "https://www.bda.ao/apoio-ao-cliente/agencias/"},
        {"_id": "BE", "website": "https://www.bancoeconomico.ao/pt/institucional/onde-estamos/"},
        {"_id": "BFA", "website": "https://www.bfa.ao/pt/particulares/lojas/"},
        {"_id": "BIC", "website": "https://www.bancobic.ao/inicio/institucional/contactos/agencias"},
        {"_id": "BIR", "website": "https://www.bir.ao/inicio/footer/onde-estamos"},
        {"_id": "BNI", "website": "https://www.bni.ao/pt/agencias"},
        {"_id": "BOCLB", "website": "https://www.bankofchina.com/ao/pt/"},
        {"_id": "BPC", "website": ""},
        {"_id": "BSOL", "website": "https://www.bancosol.ao/pt/balcoes-banco-sol"},
        {"_id": "BVB", "website": "https://www.bancovalor.ao/pages/localizar_agencia.php"},
        {"_id": "FNB", "website": ""},
        {"_id": "BKEVE", "website": "https://www.keve.ao/contactos"},
        {"_id": "SBA", "website": "https://www.standardbank.co.ao/angola/pt/sobre-nos/quem-somos/Agências"},
        {"_id": "SCBA", "website": ""},
        {"_id": "VTB", "website": "https://www.vtb.ao/Conteudos/Contactos/lista.aspx?idc=383&idsc=499&idl=1"},
        {"_id": "YETU", "website": "https://www.bancoyetu.ao/inicio/agencies"}
    ]
    
    total_updated = 0

    for update in updates:
        result = collection.update_one(
            {"_id": update["_id"]},           # Filter: find the document with this '_id'
            {"$set": {"website": update["website"]}}  # Update: set the 'website' field
        )
        print(f"Updated {result.modified_count} record(s) for _id: {update['_id']}")
        total_updated += result.modified_count

    print(f"Total records updated: {total_updated}")

except Exception as e:
    print(f"An error occurred: {e}")
