# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0026_auto_20180314_0438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worksheet',
            name='exercise_goal',
            field=models.CharField(help_text='The goal of the exercise.', max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='worksheet',
            name='exercise_goal_en',
            field=models.CharField(help_text='The goal of the exercise.', max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='worksheet',
            name='exercise_goal_ind',
            field=models.CharField(help_text='The goal of the exercise.', max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='worksheet',
            name='exercise_task',
            field=models.TextField(help_text='Task in the exercise. Markdown is supported.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='worksheet',
            name='exercise_task_en',
            field=models.TextField(help_text='Task in the exercise. Markdown is supported.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='worksheet',
            name='exercise_task_ind',
            field=models.TextField(help_text='Task in the exercise. Markdown is supported.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='worksheet',
            name='more_about_text',
            field=models.TextField(help_text='More detail about the content of the worksheet. Markdown is supported.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='worksheet',
            name='more_about_text_en',
            field=models.TextField(help_text='More detail about the content of the worksheet. Markdown is supported.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='worksheet',
            name='more_about_text_ind',
            field=models.TextField(help_text='More detail about the content of the worksheet. Markdown is supported.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='worksheet',
            name='more_about_title',
            field=models.CharField(default='More about', max_length=200, null=True, help_text='More about title.', blank=True),
        ),
        migrations.AlterField(
            model_name='worksheet',
            name='more_about_title_en',
            field=models.CharField(default='More about', max_length=200, null=True, help_text='More about title.', blank=True),
        ),
        migrations.AlterField(
            model_name='worksheet',
            name='more_about_title_ind',
            field=models.CharField(default='More about', max_length=200, null=True, help_text='More about title.', blank=True),
        ),
    ]
