# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-12 04:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_auto_20170211_2029'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lobby',
            old_name='user',
            new_name='created_by',
        ),
    ]
