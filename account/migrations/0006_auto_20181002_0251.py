# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-10-01 20:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20180802_1033'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='logo_path',
        ),
        migrations.AddField(
            model_name='organization',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='org/image/%Y/%m/%d/'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(blank=True, max_length=255, null=True),
        ),
    ]
