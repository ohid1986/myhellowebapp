# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-23 17:53
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0003_social'),
    ]

    operations = [
        migrations.AddField(
            model_name='social',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 4, 23, 17, 51, 48, 795409, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='social',
            name='updated',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 4, 23, 17, 53, 30, 949182, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='thing',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 4, 23, 17, 53, 46, 837210, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='thing',
            name='updated',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 4, 23, 17, 53, 53, 169620, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
