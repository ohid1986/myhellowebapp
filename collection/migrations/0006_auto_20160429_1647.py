# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-29 10:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0005_upload'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thing',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to=settings.AUTH_USER_MODEL),
        ),
    ]
