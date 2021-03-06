# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-07-25 16:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('join_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'ordering': ('-join_date',),
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('org_url', models.URLField(blank=True, max_length=255, null=True)),
                ('org_short_name', models.CharField(blank=True, max_length=255, null=True)),
                ('org_full_name', models.CharField(blank=True, max_length=255, null=True)),
                ('contract_holder', models.CharField(blank=True, max_length=255, null=True)),
                ('class_type', models.CharField(blank=True, max_length=255, null=True)),
                ('policy_num', models.CharField(blank=True, max_length=255, null=True)),
                ('policy_agency', models.CharField(blank=True, max_length=255, null=True)),
                ('date_fiscal_start', models.DateField(blank=True, null=True)),
                ('date_fiscal_end', models.DateField(blank=True, null=True)),
                ('num_pay_periods', models.FloatField(blank=True, null=True)),
                ('logo_path', models.CharField(blank=True, max_length=255, null=True)),
                ('enrolment_period', models.CharField(blank=True, max_length=255, null=True)),
                ('misc_1', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
