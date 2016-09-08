# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-09-08 21:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0045_auto_20160908_1418'),
    ]

    operations = [
        migrations.CreateModel(
            name='FitbitConnection',
            fields=[
                ('thirdpartyconnection_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.ThirdPartyConnection')),
                ('refresh_token', models.CharField(max_length=1000, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.User')),
            ],
            bases=('main.thirdpartyconnection',),
        ),
    ]
