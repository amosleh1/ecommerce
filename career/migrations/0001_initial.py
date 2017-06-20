# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_countries.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('first_name', models.CharField(max_length=150)),
                ('middle_name', models.CharField(max_length=150, blank=True, null=True)),
                ('last_name', models.CharField(max_length=150)),
                ('nationality', models.CharField(max_length=150)),
                ('birth_date', models.DateField()),
                ('phone', models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{8,15}$', message="Phone number must be entered in the format: '+999999'. Min of 5 digits and max Up to 15 digits allowed.")])),
                ('email', models.EmailField(max_length=50)),
                ('comment', models.CharField(max_length=500, null=True, blank=True, help_text='Please Enter any comments')),
                ('resume_file', models.FileField(upload_to='career/%Y/%m/%d/')),
                ('applied_timestamp', models.DateField(auto_now_add=True)),
            ],
            options={
                'ordering': ('applied_timestamp',),
            },
        ),
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=150, unique=True, db_index=True)),
                ('slug', models.CharField(max_length=150, unique=True)),
                ('job_summary', models.TextField(blank=True, null=True)),
                ('location', django_countries.fields.CountryField(max_length=2)),
                ('responsibilities', models.TextField(blank=True, null=True)),
                ('requirements', models.TextField(blank=True, null=True)),
                ('is_published', models.BooleanField(default=True, verbose_name='Publish?')),
                ('created_timestamp', models.DateField(auto_now_add=True)),
            ],
            options={
                'ordering': ('is_published', 'title'),
                'verbose_name_plural': 'Vacancies',
                'verbose_name': 'Vacancy',
            },
        ),
        migrations.AlterIndexTogether(
            name='vacancy',
            index_together=set([('id', 'slug')]),
        ),
        migrations.AddField(
            model_name='resume',
            name='vacancy',
            field=models.ForeignKey(to='career.Vacancy'),
        ),
    ]
