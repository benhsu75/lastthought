# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-03 01:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0031_auto_20160903_0031'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ridelogentry',
            old_name='price',
            new_name='price_in_dollars',
        ),
    ]
