import requests
import json

from django.core.management.base import BaseCommand
from oscar.apps.rajaongkir_cities.models import RajaongkirCity


class Command(BaseCommand):
    help = 'Updates RajaOngkir cities list'

    def handle(self, *args, **options):

        headers = {
            'key': "be8ff21f6c646accd40b895c219d8f66",
            'content-type': "application/x-www-form-urlencoded"
            }

        r = requests.get('http://api.rajaongkir.com/starter/city', headers=headers)
        parsed = json.loads(r.text)
        RajaongkirCity.objects.all().delete()
        cities = []
        for city in parsed['rajaongkir']['results']:
            cities.append(RajaongkirCity(
                city_id=city['city_id'],
                city_name=city['city_name'],
                postal_code=city['postal_code'],
                province=city['province'],
                province_id=city['province_id'],
                type=city['type']
            ))
        RajaongkirCity.objects.bulk_create(cities)
