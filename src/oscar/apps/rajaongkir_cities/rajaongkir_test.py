import requests
import json
import django
from models import RajaongkirCity

django.setup()
payload = {'origin': '501', 'destination': '114', 'weight': '1700', 'courier': 'jne'}

headers = {
    'key': "be8ff21f6c646accd40b895c219d8f66",
    'content-type': "application/x-www-form-urlencoded"
    }

r = requests.post('http://api.rajaongkir.com/starter/cost', data=payload, headers=headers)
r = requests.get('http://api.rajaongkir.com/starter/city', headers=headers)


parsed = json.loads(r.text)
cities = []
for city in parsed['rajaongkir']['results']:
    cities.append(RajaongkirCity(
        city_id=city['city_id'],
        city_name=city['city_name'],
        postal_code=city['province'],
        province=city['province_id'],
        type=city['type']
    ))
RajaongkirCity.objects.bulk_create(cities)
# with open('cities.json', 'w') as outfile:
#     json.dump(parsed, outfile, sort_keys=True, indent=4, ensure_ascii=False)
