# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-22 02:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pots', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeSerie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('temperature', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Temperature')),
                ('humidity', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Humidity')),
                ('luminosity', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Luminosity')),
                ('water_level', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='Water level')),
                ('pot', models.ForeignKey(blank=None, null=None, on_delete=django.db.models.deletion.CASCADE, related_name='timeseries', to='pots.Pot')),
            ],
        ),
    ]
