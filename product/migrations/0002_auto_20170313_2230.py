# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='is_published',
            field=models.BooleanField(verbose_name='Publish?', default=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(help_text='Please Enter a Generic Name', max_length=150),
        ),
    ]
