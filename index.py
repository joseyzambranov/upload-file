import requests
from dotenv import load_dotenv
import os

load_dotenv()

URL_BASE = os.environ.get("URL_BASE_SINAPSIS")

resp = requests.get(f"{URL_BASE}/contactList/default/generate-signed-upload")
data = resp.json()

data['fields']['content-type'] = 'text/plain'
image_fp = open('base2.csv', 'rb')

print(data['fields'])
resp = requests.post(data['url'], data=data['fields'], files={'file': ('base2.csv', image_fp, 'image/jpeg')})
print(resp.status_code)
print(resp.text)