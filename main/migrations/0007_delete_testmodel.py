# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-02 08:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_goalentry_binary_value'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TestModel',
        ),
    ]