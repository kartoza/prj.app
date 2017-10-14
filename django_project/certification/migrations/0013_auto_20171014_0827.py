# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certification', '0012_auto_20170922_0649'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseconvener',
            name='degree',
            field=models.CharField(help_text='Degree of the course convener, e.g. MSc.', max_length=50, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='courseconvener',
            name='title',
            field=models.CharField(help_text='Title of the course convener, e.g. Prof.', max_length=50, null=True, blank=True),
        ),
    ]
