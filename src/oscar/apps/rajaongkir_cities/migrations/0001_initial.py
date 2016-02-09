# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RajaongkirCity',
            fields=[
                ('city_id', models.IntegerField(serialize=False, primary_key=True)),
                ('city_name', models.CharField(max_length=100)),
                ('postal_code', models.CharField(max_length=10, null=True, blank=True)),
                ('province', models.CharField(max_length=100)),
                ('province_id', models.IntegerField()),
                ('type', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': 'Rajaongkir cities',
            },
        ),
    ]
