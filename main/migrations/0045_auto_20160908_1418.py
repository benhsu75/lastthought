# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-08 14:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0044_instagramlogentry'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instagramlogentry',
            name='location_id',
        ),
        migrations.RemoveField(
            model_name='instagramlogentry',
            name='location_street_address',
        ),
    ]
