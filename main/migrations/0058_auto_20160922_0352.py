# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-22 03:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0057_auto_20160921_1709'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='user',
            new_name='profile',
        ),
    ]
