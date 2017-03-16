# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-16 14:55
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('pots', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pot',
            name='identifier',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, unique=True),
        ),
    ]
