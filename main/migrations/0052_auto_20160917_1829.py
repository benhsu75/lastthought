# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-17 18:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0051_googleconnection'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activitylogentry',
            old_name='distance_miles',
            new_name='distance_km',
        ),
    ]
