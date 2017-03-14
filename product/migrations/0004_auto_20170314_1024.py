# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20170313_2240'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='Date_Added',
            new_name='date_added',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='Price',
            new_name='price',
        ),
    ]
