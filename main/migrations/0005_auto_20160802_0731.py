# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-02 07:31
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20160801_0512'),
    ]

    operations = [
        migrations.AddField(
            model_name='goalentry',
            name='response_collected',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='goalentry',
            name='sent_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 8, 2, 7, 31, 50, 530888)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='goalentry',
            name='binary_value',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='goalentry',
            name='text_value',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
