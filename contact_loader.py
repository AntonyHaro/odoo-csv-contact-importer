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
            
            column_indices = {
                "name": header.index("name"),
                "is_company": header.index("is_company"),
                "company_name": header.index("company_name"),
                "country_name": header.index("country_name"),
                "zip": header.index("zip"),
                "city": header.index("city"),
                "street": header.index("street"),
                "phone": header.index("phone"),
                "mobile": header.index("mobile"),
                "email": header.index("email"),
                "vat": header.index("vat")
            }

            contacts = []
            invalid_contacts = []
            
            print("\nRegistros válidos do arquivo:")
            for row_index, row in enumerate(reader, start=1):    
                
                contact = {
                    "name": row[column_indices["name"]].strip(),
                    "is_company": row[column_indices["is_company"]].strip(),
                    "company_name": row[column_indices["company_name"]].strip(),
                    "country_id": row[column_indices["country_name"]].strip(),
                    "zip": row[column_indices["zip"]].strip(),
                    "city": row[column_indices["city"]].strip(),
                    "street": row[column_indices["street"]].strip(),
                    "phone": row[column_indices["phone"]].strip(),
                    "mobile": row[column_indices["mobile"]].strip(),
                    "email": row[column_indices["email"]].strip(),
                    "vat": row[column_indices["vat"]].strip()
                }

                if not contact["name"] or not contact["email"]:
                    invalid_contacts.append(f"Registro {row_index}")
                    continue

                print(f"Registro {row_index}, Nome: {contact['name']}, Email: {contact['email']}")
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

        if not uid: 
            raise ValueError("Falha na autenticação. Verifique as credenciais.")
        return uid
    
    except Exception as e:
        print(f"Erro ao autenticar: {e}")

def get_country_id(models, db, uid, password, country_name):
    country_ids = models.execute_kw(db, uid, password, "res.country", "search", [[('name', '=', country_name)]])
    return country_ids[0] if country_ids else None

def create_contacts(url, db, uid, password, contacts):
    try: 
        models = xmlrpc.client.ServerProxy("{}/xmlrpc/2/object".format(url))

        for contact in contacts:
            if not contact.get("name") or not contact.get("email"):
                print(f"Contato inválido, faltando nome ou email: {contact}")
                continue

            country_id = get_country_id(models, db, uid, password, contact["country_id"])

            if country_id:
                contact["country_id"] = country_id
            else:
                print(f"País '{contact['country_id']}' não encontrado. O contato não será criado.")
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
