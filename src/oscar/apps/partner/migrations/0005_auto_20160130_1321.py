# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0004_auto_20160130_0936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partneraddress',
            name='country',
            field=models.ForeignKey(verbose_name='Country', blank=True, to='address.Country'),
        ),
    ]
