# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-04 12:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userroles', '0002_auto_20160704_1455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrole',
            name='name',
            field=models.CharField(choices=[('nobody', 'nobody'), ('watcher', 'watcher'), ('parent', 'parent'), ('child', 'child')], max_length=100),
        ),
    ]
