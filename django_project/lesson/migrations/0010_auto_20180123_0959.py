# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0009_auto_20180122_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='worksheet',
            name='more_about_title',
            field=models.TextField(default='More about', help_text='More about title.', max_length=200),
        ),
        migrations.AlterField(
            model_name='worksheet',
            name='author_name',
            field=models.CharField(help_text='The author of this worksheet.', max_length=200, null=True, blank=True),
        ),
    ]
