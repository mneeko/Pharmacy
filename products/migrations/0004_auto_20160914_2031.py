# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-14 17:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20160914_2026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(max_length=120, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='product',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='product',
            name='slug',
        ),
    ]
