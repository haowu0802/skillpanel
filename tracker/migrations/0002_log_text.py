# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-31 01:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='text',
            field=models.TextField(default=''),
        ),
    ]
