# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-09 01:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0046_fitbitconnection'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeightLogEntry',
            fields=[
                ('logentry_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.LogEntry')),
                ('source_type', models.SmallIntegerField()),
            ],
            bases=('main.logentry',),
        ),
        migrations.AddField(
            model_name='fitbitconnection',
            name='fitbit_id',
            field=models.CharField(default=None, max_length=200),
            preserve_default=False,
        ),
    ]
