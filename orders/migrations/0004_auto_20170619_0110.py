# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20170619_0059'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='Country',
            new_name='country',
        ),
    ]
