# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-24 18:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0060_profile_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='utc_offset',
            field=models.IntegerField(default=-4),
            preserve_default=False,
        ),
    ]
