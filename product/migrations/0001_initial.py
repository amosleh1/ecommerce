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
                ('name', models.CharField(help_text='Please Enter A Name', max_length=150, unique=True)),
                ('slug', models.CharField(max_length=150, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='category/Media/%Y/%m/%d')),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(help_text='Please Enter a Generic Name', max_length=200)),
                ('model', models.CharField(max_length=70, blank=True, null=True)),
                ('slug', models.CharField(max_length=200, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, upload_to='product/Media/%Y/%m/%d')),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('stock', models.PositiveIntegerField(blank=True, null=True)),
                ('show_stock', models.BooleanField(default=False, verbose_name='Show Stock Quantity?')),
                ('is_published', models.BooleanField(default=True, verbose_name='Publish?')),
                ('is_discounted', models.BooleanField(default=False, verbose_name='With Discount Offer?')),
                ('discount_expire', models.DateTimeField(verbose_name='Last Date for Discount', null=True, blank=True)),
                ('discounted_price', models.DecimalField(max_digits=10, verbose_name='After Discount Price', null=True, blank=True, decimal_places=2)),
                ('is_featured', models.BooleanField(default=False, verbose_name='Fetured Product?')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('categories', models.ManyToManyField(to='product.Category', related_name='products')),
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
