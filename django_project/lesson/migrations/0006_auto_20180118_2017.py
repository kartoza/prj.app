# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0005_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='specification',
            name='slug',
            field=models.SlugField(default=datetime.datetime(2018, 1, 18, 18, 17, 52, 285116, tzinfo=utc)),
            preserve_default=False,
        ),
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
        migrations.AlterField(
            model_name='specification',
            name='specification_number',
            field=models.IntegerField(default=0, help_text='Used to order the specifications for a lesson into the correct sequence.'),
        ),
        migrations.AlterUniqueTogether(
            name='specification',
            unique_together=set([]),
        ),
    ]
