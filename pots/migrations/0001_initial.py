# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-13 03:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('plants', '0001_initial'),
        ('places', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('place', models.ForeignKey(blank=None, null=None, on_delete=django.db.models.deletion.CASCADE, related_name='pots', to='places.Place')),
                ('plant', models.ForeignKey(blank=None, null=None, on_delete=django.db.models.deletion.CASCADE, related_name='pots', to='plants.Plant')),
            ],
        ),
    ]
