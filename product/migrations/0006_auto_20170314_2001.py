# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_auto_20170314_1949'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='categrories',
            new_name='categories',
        ),
    ]
