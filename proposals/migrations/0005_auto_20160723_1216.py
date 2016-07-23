# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-23 12:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0004_auto_20160711_2058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='talk',
            name='event',
            field=models.IntegerField(choices=[(1, 'conference short'), (2, 'conference long'), (3, 'workshop'), (4, 'stand'), (5, 'other')], default=1, verbose_name='Format'),
        ),
        migrations.AlterField(
            model_name='talk',
            name='speakers',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Speakers'),
        ),
        migrations.AlterField(
            model_name='talk',
            name='topics',
            field=models.ManyToManyField(blank=True, to='proposals.Topic', verbose_name='Topics'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='reviewers',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='Reviewers'),
        ),
    ]