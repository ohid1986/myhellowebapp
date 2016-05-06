# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-01 09:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0006_auto_20160429_1647'),
    ]

    operations = [
        migrations.AddField(
            model_name='thing',
            name='stripe_id',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='thing',
            name='upgraded',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='thing',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
