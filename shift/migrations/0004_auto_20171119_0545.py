# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-19 05:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shift', '0003_delete_employee'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='run',
            name='shift',
        ),
        migrations.DeleteModel(
            name='Run',
        ),
        migrations.DeleteModel(
            name='Shift',
        ),
    ]
