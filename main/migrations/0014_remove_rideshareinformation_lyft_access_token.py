# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-13 05:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20160809_0702'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rideshareinformation',
            name='lyft_access_token',
        ),
    ]
