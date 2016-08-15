# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-15 01:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_auto_20160814_2350'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('log', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Log')),
                ('log_context', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.LogContext')),
            ],
        ),
        migrations.RemoveField(
            model_name='imagelogentry',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='imagelogentry',
            name='id',
        ),
        migrations.RemoveField(
            model_name='imagelogentry',
            name='log',
        ),
        migrations.RemoveField(
            model_name='imagelogentry',
            name='log_context',
        ),
        migrations.RemoveField(
            model_name='imagelogentry',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='numericlogentry',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='numericlogentry',
            name='id',
        ),
        migrations.RemoveField(
            model_name='numericlogentry',
            name='log',
        ),
        migrations.RemoveField(
            model_name='numericlogentry',
            name='log_context',
        ),
        migrations.RemoveField(
            model_name='numericlogentry',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='textlogentry',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='textlogentry',
            name='id',
        ),
        migrations.RemoveField(
            model_name='textlogentry',
            name='log',
        ),
        migrations.RemoveField(
            model_name='textlogentry',
            name='log_context',
        ),
        migrations.RemoveField(
            model_name='textlogentry',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='imagelogentry',
            name='logentry_ptr',
            field=models.OneToOneField(auto_created=True, default=None, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.LogEntry'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='numericlogentry',
            name='logentry_ptr',
            field=models.OneToOneField(auto_created=True, default=None, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.LogEntry'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='textlogentry',
            name='logentry_ptr',
            field=models.OneToOneField(auto_created=True, default=None, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='main.LogEntry'),
            preserve_default=False,
        ),
    ]
