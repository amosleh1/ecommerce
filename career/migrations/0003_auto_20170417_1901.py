# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('career', '0002_auto_20170414_1239'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vacancy',
            name='expiration_date',
        ),
        migrations.AlterField(
            model_name='resume',
            name='resume_file',
            field=models.FileField(upload_to='career/%Y/%m/%d/'),
        ),
    ]
