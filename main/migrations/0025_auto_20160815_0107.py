# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-15 01:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_logcontext_entry_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logcontext',
            name='entry_type',
        ),
        migrations.AddField(
            model_name='logentry',
            name='entry_type',
            field=models.SmallIntegerField(default=1),
            preserve_default=False,
        ),
    ]
