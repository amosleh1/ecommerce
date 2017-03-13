# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=150)),
                ('model', models.CharField(blank=True, max_length=70, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('Price', models.IntegerField()),
                ('is_published', models.BooleanField(default=False)),
                ('Date_Added', models.DateTimeField()),
            ],
        ),
    ]
