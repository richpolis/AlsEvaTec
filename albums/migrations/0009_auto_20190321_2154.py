# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-21 21:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('albums', '0008_auto_20190321_2139'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='ntracks',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='album',
            name='year',
            field=models.IntegerField(default=2019),
        ),
        migrations.AlterField(
            model_name='album',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='album',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
