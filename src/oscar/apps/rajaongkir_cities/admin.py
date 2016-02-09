from django.contrib import admin
from oscar.core.loading import get_model

RajaongkirCity = get_model('rajaongkir_cities', 'RajaongkirCity')


class RajaongkirCityAdmin(admin.ModelAdmin):
    list_display = ['city_id', 'city_name', 'postal_code', 'province', 'province_id', 'type']


admin.site.register(RajaongkirCity, RajaongkirCityAdmin)
