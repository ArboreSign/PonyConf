# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-13 19:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_auto_20161013_1922'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(blank=True, default='', max_length=16, verbose_name='Phone number'),
        ),
    ]
