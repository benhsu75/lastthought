# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-10 04:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0047_auto_20160909_0157'),
    ]

    operations = [
        migrations.AddField(
            model_name='weightlogentry',
            name='metric_weight',
            field=models.FloatField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='weightlogentry',
            name='source_id',
            field=models.CharField(default=None, max_length=200),
            preserve_default=False,
        ),
    ]
