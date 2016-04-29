# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-29 10:21
from __future__ import unicode_literals

import collection.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0004_auto_20160423_2353'),
    ]

    operations = [
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=collection.models.get_image_path)),
                ('thing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uploads', to='collection.Thing')),
            ],
        ),
    ]