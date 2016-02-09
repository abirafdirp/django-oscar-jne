# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productreview',
            name='status',
            field=models.SmallIntegerField(default=0, verbose_name='Status', choices=[(0, 'Requires moderation'), (1, 'Approved'), (2, 'Rejected')]),
        ),
    ]
