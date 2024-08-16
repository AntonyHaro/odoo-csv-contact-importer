import xmlrpc.client
import csv
import os
from dotenv import load_dotenv
load_dotenv()

def import_csv_contacts(file_name):
    print(f"Diretório atual: {os.getcwd()}")
    
    try:
        if not os.path.isfile(file_name):
            print(f"Arquivo '{file_name}' não encontrado no diretório atual.")
            return
        
        with open(file_name, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)
            
            email_index = header.index("Email")
            name_index = header.index("Name")
            city_index = header.index("City")
            street_index = header.index("Street")
            cpf_index = header.index("CPF")
            zipcode_index = header.index("Zip")
            country_index = header.index("Country")
            
            contacts = []
            invalid_contacts = []
            
            print("\nRegistros válidos do arquivo:")
            for row_index, row in enumerate(reader, start=1):    
                name = row[name_index]
                email = row[email_index]
                
                if not name or not email:
                    invalid_contacts.append(f"Registro {row_index}")
                    continue
                
                print(f"Registro {row_index}, Nome: {row[name_index]}, Email: {row[email_index]}")
                
                contact = {
                    "name": row[name_index],
                    "email": row[email_index],
                    "city": row[city_index],
                    "street": row[street_index],
                    "vat": row[cpf_index],  
                    "zip": row[zipcode_index],
                    "country_id": int(row[country_index]),  
                }
                contacts.append(contact)
            
            if len(invalid_contacts) > 0:
                print("\nRegistros inválidos:")
                for i in invalid_contacts:
                    print(i)
            
            return contacts

    except Exception as e:
        print(f"Erro ao carregar o arquivo: {e}")
        
def authenticate(url, db, username, password):
    try:
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})

        if uid:
            print(f"Autenticação feita com sucesso. UID: {uid}")
        else: 
            raise ValueError("Falha na autenticação. Verifique as credenciais.")
        return uid
    
    except Exception as e:
        print(f"Erro ao autenticar: {e}")

def create_contacts(url, db, uid, password, contacts):
    try: 
        models = xmlrpc.client.ServerProxy("{}/xmlrpc/2/object".format(url))

        for contact in contacts:
            if not contact.get("name") or not contact.get("email"):
                print(f"Contato inválido, faltando nome ou email: {contact}")
                continue
            
            contact_id = models.execute_kw(db, uid, password, "res.partner", "create", [contact])
            print(f"Contato criado com o ID: {contact_id}")
        
    except Exception as e:
        print(f"Erro ao criar contatos: {e}")

def main():
    odoo_url = os.getenv("ODOO_URL")
    odoo_db = os.getenv("ODOO_DB")
    odoo_username = os.getenv("ODOO_USERNAME")
    odoo_password = os.getenv("ODOO_PASSWORD")

    uid = authenticate(odoo_url, odoo_db, odoo_username, odoo_password)
    if uid:
        contacts = import_csv_contacts("file.csv")
        
        if contacts:
            print(f"\nTotal de contatos para serem carregados: {len(contacts)}\n")
            create_contacts(odoo_url, odoo_db, uid, odoo_password, contacts)
    
if __name__ == "__main__":
    main()
