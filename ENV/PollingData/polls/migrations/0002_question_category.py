# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-06-24 15:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='category',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
