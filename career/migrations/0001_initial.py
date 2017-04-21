# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=150)),
                ('middle_name', models.CharField(null=True, max_length=150, blank=True)),
                ('last_name', models.CharField(max_length=150)),
                ('nationality', django_countries.fields.CountryField(max_length=2)),
                ('birth_date', models.DateField()),
                ('phone', models.CharField(validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{8,15}$', message="Phone number must be entered in the format: '+999999'. Min of 5 digits and max Up to 15 digits allowed.")], max_length=16)),
                ('email', models.EmailField(max_length=50)),
                ('comment', models.CharField(null=True, max_length=500, help_text='Please Enter any comments', blank=True)),
                ('resume_file', models.FileField(help_text='Please upload resume (max 4mb using (pdf, doc, docx)', upload_to='career/%Y/%m/%d/')),
                ('applied_timestamp', models.DateField(auto_now_add=True)),
            ],
            options={
                'ordering': ('applied_timestamp',),
            },
        ),
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(unique=True, max_length=150, db_index=True)),
                ('slug', models.CharField(max_length=150, unique=True)),
                ('job_summary', models.TextField(null=True, blank=True)),
                ('location', django_countries.fields.CountryField(max_length=2)),
                ('responsibilities', models.TextField(null=True, blank=True)),
                ('requirements', models.TextField(null=True, blank=True)),
                ('is_published', models.BooleanField(default=True, verbose_name='Publish?')),
                ('created_timestamp', models.DateField(auto_now_add=True)),
                ('expiration_date', models.DateField(null=True, verbose_name='Last Date for Apply', blank=True)),
            ],
            options={
                'ordering': ('is_published', 'title'),
                'verbose_name': 'Vacancy',
                'verbose_name_plural': 'Vacancies',
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
