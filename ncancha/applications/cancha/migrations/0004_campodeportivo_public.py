# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-30 16:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cancha', '0003_campodeportivo_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='campodeportivo',
            name='public',
            field=models.BooleanField(default=True),
        ),
    ]
