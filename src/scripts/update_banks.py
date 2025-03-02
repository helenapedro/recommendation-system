from helpers.db_connection import client

try:
    # Access the database and collection
    db = client['recommendation-db']
    collection = db['banks']
    
    # Update data in the collection
    result = collection.update_many(
        {"_id": "ATL"}, {"$set": {"website": "https://www.atlantico.ao/pt/institucional/onde-estamos"}},
        {"_id": "BAI"}, {"$set": {"website": "https://www.bancobai.ao/pt/pontos/agencias"}},
        {"_id": "BCA"}, {"$set": {"website": ""}},
        {"_id": "BCGA"}, {"$set": {"website": "https://www.caixaangola.ao/institucional/rede-de-agencias"}},
        {"_id": "BCH"}, {"$set": {"website": "https://www.bch.co.ao/inicio/onde-estamos"}},
        {"_id": "BCI"}, {"$set": {"website": "https://www.bci.ao/particular/contactos"}},
        {"_id": "BCS"}, {"$set": {"website": "https://www.bancobcs.ao/quem-somos/o-banco/onde-estamos"}},
        {"_id": "BDA"}, {"$set": {"website": "https://www.bda.ao/apoio-ao-cliente/agencias/"}},
        {"_id": "BE"}, {"$set": {"website": "https://www.bancoeconomico.ao/pt/institucional/onde-estamos/"}},
        {"_id": "BFA"}, {"$set": {"website": "https://www.bfa.ao/pt/particulares/lojas/"}},
        {"_id": "BIC"}, {"$set": {"website": "https://www.bancobic.ao/inicio/institucional/contactos/agencias"}},
        {"_id": "BIR"}, {"$set": {"website": "https://www.bir.ao/inicio/footer/onde-estamos"}},
        {"_id": "BNI"}, {"$set": {"website": "https://www.bni.ao/pt/agencias"}},
        {"_id": "BOCLB"}, {"$set": {"website": "https://www.bankofchina.com/ao/pt/"}},
        {"_id": "BPC"}, {"$set": {"website": ""}},
        {"_id": "BSOL"}, {"$set": {"website": "https://www.bancosol.ao/pt/balcoes-banco-sol"}},
        {"_id": "BVB"}, {"$set": {"website": "https://www.bancovalor.ao/pages/localizar_agencia.php"}},
        {"_id": "FNB"}, {"$set": {"website": ""}},
        {"_id": "BKEVE"}, {"$set": {"website": "https://www.keve.ao/contactos"}},
        {"_id": "SBA"}, {"$set": {"website": "https://www.standardbank.co.ao/angola/pt/sobre-nos/quem-somos/Ag%C3%AAncias"}},
        {"_id": "SCBA"}, {"$set": {"website": ""}},
        {"_id": "VTB"}, {"$set": {"website": "https://www.vtb.ao/Conteudos/Contactos/lista.aspx?idc=383&idsc=499&idl=1"}},
        {"_id": "YETU"}, {"$set": {"website": "https://www.bancoyetu.ao/inicio/agencies"}}
        
    )
    print(f"Updated {result.modified_count} record successfully!")

except Exception as e:
    print(f"An error occurred: {e}")
