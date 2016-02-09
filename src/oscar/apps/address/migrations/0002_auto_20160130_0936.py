# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0001_initial'),
        ('rajaongkir_cities', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraddress',
            name='line4',
            field=models.ForeignKey(verbose_name='City', to='rajaongkir_cities.RajaongkirCity'),
        ),
    ]
