# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-09 20:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Plant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('description', models.TextField(verbose_name='Description')),
                ('humidity_spec', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Humidity spec')),
                ('luminosity_spec', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Luminosity spec')),
                ('temperature_spec', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Temperature spec')),
            ],
        ),
    ]
