# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-06-24 22:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_auto_20190624_1156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='polls.Category'),
        ),
    ]