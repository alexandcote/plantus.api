# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-02 20:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pots', '0004_auto_20170317_1433'),
    ]

    operations = [
        migrations.AddField(
            model_name='pot',
            name='picture',
            field=models.ImageField(default='default/pot.jpg', upload_to='pots'),
        ),
    ]
