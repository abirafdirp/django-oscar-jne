# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0005_auto_20160130_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partneraddress',
            name='country',
            field=models.ForeignKey(verbose_name='Country', blank=True, to='address.Country', null=True),
        ),
    ]
