# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20170614_0212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='email_is_verified',
            field=models.BooleanField(default=False, verbose_name='Email is verified by user'),
        ),
    ]
