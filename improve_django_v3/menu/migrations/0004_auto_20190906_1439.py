# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2019-09-06 21:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_auto_20190905_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='ingredients',
            field=models.ManyToManyField(related_name='items', to='menu.Ingredient'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='items',
            field=models.ManyToManyField(related_name='menus', to='menu.Item'),
        ),
    ]