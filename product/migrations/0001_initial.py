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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=150, unique=True, help_text='Please Enter A Name')),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('image', models.ImageField(null=True, upload_to='category/Media/%Y/%m/%d', blank=True)),
                ('description', models.TextField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=200, help_text='Please Enter a Generic Name')),
                ('model', models.CharField(max_length=70, null=True, blank=True)),
                ('slug', models.SlugField(max_length=200)),
                ('description', models.TextField(null=True, blank=True)),
                ('image', models.ImageField(blank=True, upload_to='product/Media/%Y/%m/%d')),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('discounted_price', models.DecimalField(null=True, max_digits=10, verbose_name='After Discount Price', decimal_places=2, blank=True)),
                ('stock', models.PositiveIntegerField(null=True, blank=True)),
                ('show_stock', models.BooleanField(default=False, verbose_name='Show Stock Quantity?')),
                ('is_published', models.BooleanField(default=True, verbose_name='Publish?')),
                ('is_discounted', models.BooleanField(default=True, verbose_name='With Discount Offer?')),
                ('discount_expire', models.DateTimeField(null=True, verbose_name='Last Date for Discount', blank=True)),
                ('created', models.DateTimeField(null=True, auto_now_add=True)),
                ('updated', models.DateTimeField(null=True, auto_now=True)),
                ('categories', models.ManyToManyField(related_name='products', to='product.Category')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.AlterIndexTogether(
            name='category',
            index_together=set([('id', 'slug')]),
        ),
        migrations.AlterIndexTogether(
            name='product',
            index_together=set([('id', 'slug')]),
        ),
    ]
