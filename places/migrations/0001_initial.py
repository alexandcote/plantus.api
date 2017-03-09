# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-09 22:23
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('identifier', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('users', models.ManyToManyField(blank=True, related_name='places', to='authentication.User')),
            ],
        ),
    ]
