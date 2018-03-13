# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0023_auto_20180308_0200'),
    ]

    operations = [
        migrations.AddField(
            model_name='worksheet',
            name='more_about_title_en',
            field=models.CharField(default='More about', max_length=200, null=True, help_text='More about title.'),
        ),
        migrations.AddField(
            model_name='worksheet',
            name='more_about_title_ind',
            field=models.CharField(default='More about', max_length=200, null=True, help_text='More about title.'),
        ),
    ]
