# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-06 01:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0039_uberconnection'),
    ]

    operations = [
        migrations.AddField(
            model_name='ridelogentry',
            name='city_lat',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='ridelogentry',
            name='city_lng',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='ridelogentry',
            name='city_name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='ridelogentry',
            name='distance',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='ridelogentry',
            name='end_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='ridelogentry',
            name='start_city_lat',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='ridelogentry',
            name='start_city_lng',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='ridelogentry',
            name='start_city_name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='ridelogentry',
            name='start_time',
            field=models.DateTimeField(null=True),
        ),
    ]
