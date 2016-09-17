# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-17 07:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0049_dose_glucoselog_insulinamount'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityLogEntry',
            fields=[
                ('logentry_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.LogEntry')),
                ('source_type', models.SmallIntegerField()),
                ('num_steps', models.IntegerField(null=True)),
                ('distance_miles', models.FloatField(null=True)),
                ('num_calories', models.IntegerField(null=True)),
            ],
            bases=('main.logentry',),
        ),
    ]