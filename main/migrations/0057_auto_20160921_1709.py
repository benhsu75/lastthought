# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-21 17:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0056_profile_global_fbid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='habit',
            old_name='user',
            new_name='profile',
        ),
    ]
