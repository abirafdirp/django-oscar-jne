# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_auto_20160130_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billingaddress',
            name='country',
            field=models.ForeignKey(verbose_name='Country', blank=True, to='address.Country', null=True),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='country',
            field=models.ForeignKey(verbose_name='Country', blank=True, to='address.Country', null=True),
        ),
    ]
