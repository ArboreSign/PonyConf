# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-13 19:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('volunteers', '0003_auto_20161024_1313'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activity',
            options={'verbose_name': 'Activity', 'verbose_name_plural': 'Activities'},
        ),
    ]
