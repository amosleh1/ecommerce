# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('first_name', models.CharField(max_length=150)),
                ('middle_name', models.CharField(max_length=150, blank=True, null=True)),
                ('last_name', models.CharField(max_length=150)),
                ('phone', models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{8,15}$', message="Phone number must be entered in the format: '+999999'. Min of 5 digits and max Up to 15 digits allowed.")])),
                ('email', models.EmailField(max_length=50, blank=True, null=True)),
                ('message', models.CharField(max_length=500, help_text='Please Enter your message')),
                ('message_type', models.CharField(max_length=30, choices=[('Business Offer', 'Business Offer'), ('Complain', 'Complain'), ('Question', 'Question')])),
                ('applied_timestamp', models.DateField(auto_now_add=True)),
            ],
            options={
                'ordering': ('applied_timestamp',),
            },
        ),
    ]
