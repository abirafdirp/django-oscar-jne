# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0003_auto_20150604_1450'),
        ('rajaongkir_cities', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partneraddress',
            name='line4',
            field=models.ForeignKey(verbose_name='City', to='rajaongkir_cities.RajaongkirCity'),
        ),
    ]
