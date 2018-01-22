# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0005_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='specification',
            name='value_ind',
            field=models.CharField(help_text='Value of specification.', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='worksheet',
            name='exercise_goal_ind',
            field=models.CharField(help_text='The goal of the exercise.', max_length=200, null=True),
        ),
    ]
