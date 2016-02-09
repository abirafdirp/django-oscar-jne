# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20150113_1629'),
        ('rajaongkir_cities', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billingaddress',
            name='line4',
            field=models.ForeignKey(verbose_name='City', to='rajaongkir_cities.RajaongkirCity'),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='line4',
            field=models.ForeignKey(verbose_name='City', to='rajaongkir_cities.RajaongkirCity'),
        ),
    ]
