# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-21 22:36
from __future__ import unicode_literals

import autoslug.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        ('proposals', '0010_auto_20160822_1010'),
    ]

    operations = [
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='name')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sites.Site')),
            ],
        ),
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ('pk',)},
        ),
        migrations.AlterField(
            model_name='talk',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proposals.Event', verbose_name='Intervention kind'),
        ),
        migrations.AddField(
            model_name='talk',
            name='track',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proposals.Track', verbose_name='Track'),
        ),
        migrations.AlterUniqueTogether(
            name='track',
            unique_together=set([('site', 'name')]),
        ),
    ]
