# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-16 06:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_auto_20160815_0107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='text',
            field=models.CharField(max_length=2000, null=True),
        ),
    ]
