# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-08-02 10:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_memberupload'),
    ]

    operations = [
        migrations.RenameField(
            model_name='memberupload',
            old_name='front_image',
            new_name='member_file',
        ),
    ]