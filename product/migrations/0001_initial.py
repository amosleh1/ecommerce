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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Please Enter A Name', max_length=150, unique=True)),
                ('slug', models.CharField(max_length=150, unique=True)),
                ('image', models.ImageField(null=True, blank=True, upload_to='category/Media/%Y/%m/%d')),
                ('description', models.TextField(null=True, blank=True)),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Please Enter a Generic Name', max_length=200)),
                ('model', models.CharField(null=True, max_length=70, blank=True)),
                ('slug', models.CharField(max_length=200, unique=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('image', models.ImageField(blank=True, upload_to='product/Media/%Y/%m/%d')),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('stock', models.PositiveIntegerField(null=True, blank=True)),
                ('show_stock', models.BooleanField(default=False, verbose_name='Show Stock Quantity?')),
                ('is_published', models.BooleanField(default=True, verbose_name='Publish?')),
                ('is_discounted', models.BooleanField(default=False, verbose_name='With Discount Offer?')),
                ('discount_expire', models.DateTimeField(null=True, verbose_name='Last Date for Discount', blank=True)),
                ('discounted_price', models.DecimalField(max_digits=10, null=True, verbose_name='After Discount Price', decimal_places=2, blank=True)),
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
