from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models


@python_2_unicode_compatible
class RajaongkirCity(models.Model):
    city_id = models.IntegerField(primary_key=True)
    city_name = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    province = models.CharField(max_length=100)
    province_id = models.IntegerField()
    type = models.CharField(max_length=30)

    def __str__(self):
        return self.city_name

    class Meta:
        verbose_name_plural = "Rajaongkir cities"
