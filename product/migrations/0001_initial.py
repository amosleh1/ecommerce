# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(unique=True, help_text='Please Enter A Name', max_length=150)),
                ('slug', models.SlugField(blank=True, unique=True, max_length=200, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'categories',
                'verbose_name': 'category',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(help_text='Please Enter a Generic Name', max_length=200)),
                ('model', models.CharField(blank=True, max_length=70, null=True)),
                ('slug', models.SlugField(blank=True, max_length=200, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, upload_to='products/%Y/%m/%d')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock', models.PositiveIntegerField(blank=True, null=True)),
                ('available', models.BooleanField(default=True)),
                ('is_published', models.BooleanField(default=False, verbose_name='Publish?')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('categories', models.ManyToManyField(related_name='products', to='product.Category')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
    ]
