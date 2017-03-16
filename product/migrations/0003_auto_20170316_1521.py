# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20170316_1517'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='category',
            index_together=set([('id', 'slug')]),
        ),
        migrations.AlterIndexTogether(
            name='product',
            index_together=set([('id', 'slug')]),
        ),
    ]
