# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2019-09-05 21:11
from __future__ import unicode_literals

from django.db import migrations, models
import menu.models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_auto_20160406_1554'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='menu',
            options={'ordering': ['expiration_date', 'season']},
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='menu',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='menu',
            name='expiration_date',
            field=models.DateTimeField(default=menu.models.set_expiry_date),
        ),
        migrations.AlterField(
            model_name='menu',
            name='season',
            field=models.CharField(max_length=200),
        ),
    ]
