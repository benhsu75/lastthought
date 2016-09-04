# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-03 03:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0033_auto_20160903_0332'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocationLogEntry',
            fields=[
                ('logentry_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.LogEntry')),
                ('lat', models.FloatField()),
                ('lng', models.FloatField()),
                ('name', models.CharField(max_length=200)),
                ('comment', models.CharField(max_length=1000)),
            ],
            bases=('main.logentry',),
        ),
    ]