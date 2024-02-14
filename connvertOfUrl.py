import requests
from dotenv import load_dotenv
import os
import csv
from io import StringIO
import json

load_dotenv()

URL_BASE = os.environ.get("URL_BASE_SINAPSIS_2")
URL_BASE_AWS = os.environ.get("URL_BASE_AWS")

csv_url = URL_BASE_AWS
response = requests.get(csv_url)

if response.status_code == 200:
    csv_content = response.content.decode('utf-8')
    
    csv_file = StringIO(csv_content)
    csv_in = csv.DictReader(csv_file)
    
    converted_rows = []
    for row in csv_in:
        converted_row = {
            "emailAddress": row["CORREO"],
            "unsubscribeAll": "false"
        }
        converted_rows.append(converted_row)
    
    resp_generate = requests.get(f"{URL_BASE}/contactList/default/generate-signed-upload")
    data = resp_generate.json()
    data['fields']['content-type'] = 'text/plain'
    csv_output = StringIO()
    csv_out = csv.DictWriter(csv_output, fieldnames=["emailAddress", "unsubscribeAll"])
    csv_out.writeheader()
    csv_out.writerows(converted_rows)
    
    csv_file = {'file': ('base2.csv', csv_output.getvalue())}
    #print(data['fields'])
    print(data['fields']['key'])
    resp_upload = requests.post(data['url'], data=data['fields'], files=csv_file)
    print(resp_upload.status_code)
    
    if resp_upload.status_code in [200, 204]:
        import_url = f"{URL_BASE}/contactList/default/import-job"
        import_body = {
            "s3Key": data['fields']['key']
        }
        import_headers = {'Content-Type': 'application/json'}
        
        # Realizar la solicitud POST para cargar el key en la otra URL
        resp_import = requests.post(import_url, data=json.dumps(import_body), headers=import_headers)
        
        # Verificar si la solicitud POST fue exitosa
        if resp_import.status_code == 200:
            print("El key se ha cargado exitosamente en la otra URL.")
        else:
            print("Error al cargar el key en la otra URL.")
        

else:
    print("Error al descargar el archivo CSV desde la URL.")
