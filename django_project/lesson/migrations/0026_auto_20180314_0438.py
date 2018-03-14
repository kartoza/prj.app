# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0025_auto_20180313_0955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='answer_explanation',
            field=models.TextField(help_text='Answer explanation. Markdown is supported.', blank=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='answer_explanation_en',
            field=models.TextField(help_text='Answer explanation. Markdown is supported.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='answer_explanation_ind',
            field=models.TextField(help_text='Answer explanation. Markdown is supported.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='section',
            name='notes',
            field=models.TextField(help_text='Section notes.', verbose_name='Section notes. Markdown is supported.'),
        ),
        migrations.AlterField(
            model_name='section',
            name='notes_en',
            field=models.TextField(help_text='Section notes.', null=True, verbose_name='Section notes. Markdown is supported.'),
        ),
        migrations.AlterField(
            model_name='section',
            name='notes_ind',
            field=models.TextField(help_text='Section notes.', null=True, verbose_name='Section notes. Markdown is supported.'),
        ),
        migrations.AlterField(
            model_name='worksheet',
            name='exercise_task',
            field=models.TextField(help_text='Task in the exercise. Markdown is supported.'),
        ),
        migrations.AlterField(
            model_name='worksheet',
            name='exercise_task_en',
            field=models.TextField(help_text='Task in the exercise. Markdown is supported.', null=True),
        ),
        migrations.AlterField(
            model_name='worksheet',
            name='exercise_task_ind',
            field=models.TextField(help_text='Task in the exercise. Markdown is supported.', null=True),
        ),
    ]
