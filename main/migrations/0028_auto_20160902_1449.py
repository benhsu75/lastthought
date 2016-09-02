# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-02 14:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0027_auto_20160817_0450'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagelogentry',
            name='image_height',
            field=models.SmallIntegerField(default=360),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='imagelogentry',
            name='image_width',
            field=models.SmallIntegerField(default=640),
            preserve_default=False,
        ),
    ]