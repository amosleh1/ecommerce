# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_auto_20170314_1024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='date_added',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
