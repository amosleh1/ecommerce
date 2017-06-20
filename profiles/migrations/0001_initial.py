# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_countries.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(verbose_name='last login', null=True, blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('date_joined', models.DateTimeField(verbose_name='date joined', auto_now_add=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('is_admin', models.BooleanField(default=False)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='profile/Media/avatar/')),
                ('phone', models.CharField(max_length=16, blank=True, null=True, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{8,15}$', message="Phone number must be entered in the format: '+999999'. Min of 5 digits and max Up to 15 digits allowed.")])),
                ('gender', models.CharField(default='', max_length=40, choices=[('man', 'Man'), ('female', 'Female')], verbose_name='Gender', blank=True)),
                ('nationality', django_countries.fields.CountryField(default='', max_length=2, blank=True)),
                ('completion_level', models.PositiveSmallIntegerField(default=0, verbose_name='Profile completion percentage')),
                ('email_is_verified', models.BooleanField(default=False, verbose_name='Email is verified')),
                ('personal_info_is_completed', models.BooleanField(default=False, verbose_name='Personal info completed')),
                ('groups', models.ManyToManyField(help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', to='auth.Group', blank=True, related_name='user_set', verbose_name='groups', related_query_name='user')),
                ('user_permissions', models.ManyToManyField(help_text='Specific permissions for this user.', to='auth.Permission', blank=True, related_name='user_set', verbose_name='user permissions', related_query_name='user')),
            ],
            options={
                'verbose_name': 'user profile',
                'verbose_name_plural': 'user profiles',
            },
        ),
    ]
