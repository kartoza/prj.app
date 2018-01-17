# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0003_auto_20180117_0349'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='answer_af',
            field=models.CharField(help_text='Answer.', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='answer_en',
            field=models.CharField(help_text='Answer.', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='answer_explanation_af',
            field=models.TextField(help_text='Answer explanation.', max_length=1000, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='answer_explanation_en',
            field=models.TextField(help_text='Answer explanation.', max_length=1000, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='answer_explanation_ind',
            field=models.TextField(help_text='Answer explanation.', max_length=1000, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='answer_explanation_ko',
            field=models.TextField(help_text='Answer explanation.', max_length=1000, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='answer_ind',
            field=models.CharField(help_text='Answer.', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='answer_ko',
            field=models.CharField(help_text='Answer.', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='furtherreading',
            name='text_af',
            field=models.CharField(help_text='Text of the further reading.', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='furtherreading',
            name='text_en',
            field=models.CharField(help_text='Text of the further reading.', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='furtherreading',
            name='text_ind',
            field=models.CharField(help_text='Text of the further reading.', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='furtherreading',
            name='text_ko',
            field=models.CharField(help_text='Text of the further reading.', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='section',
            name='name_af',
            field=models.CharField(help_text='Name of section.', max_length=200, null=True, verbose_name='Name of section'),
        ),
        migrations.AddField(
            model_name='section',
            name='name_en',
            field=models.CharField(help_text='Name of section.', max_length=200, null=True, verbose_name='Name of section'),
        ),
        migrations.AddField(
            model_name='section',
            name='name_ind',
            field=models.CharField(help_text='Name of section.', max_length=200, null=True, verbose_name='Name of section'),
        ),
        migrations.AddField(
            model_name='section',
            name='name_ko',
            field=models.CharField(help_text='Name of section.', max_length=200, null=True, verbose_name='Name of section'),
        ),
        migrations.AddField(
            model_name='section',
            name='notes_af',
            field=models.TextField(help_text='Section notes.', max_length=1000, null=True, verbose_name='Section notes.'),
        ),
        migrations.AddField(
            model_name='section',
            name='notes_en',
            field=models.TextField(help_text='Section notes.', max_length=1000, null=True, verbose_name='Section notes.'),
        ),
        migrations.AddField(
            model_name='section',
            name='notes_ind',
            field=models.TextField(help_text='Section notes.', max_length=1000, null=True, verbose_name='Section notes.'),
        ),
        migrations.AddField(
            model_name='section',
            name='notes_ko',
            field=models.TextField(help_text='Section notes.', max_length=1000, null=True, verbose_name='Section notes.'),
        ),
        migrations.AddField(
            model_name='specification',
            name='notes_af',
            field=models.CharField(help_text='Notes of specification.', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='specification',
            name='notes_en',
            field=models.CharField(help_text='Notes of specification.', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='specification',
            name='notes_ind',
            field=models.CharField(help_text='Notes of specification.', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='specification',
            name='notes_ko',
            field=models.CharField(help_text='Notes of specification.', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='specification',
            name='title_af',
            field=models.CharField(help_text='Title of specification.', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='specification',
            name='title_en',
            field=models.CharField(help_text='Title of specification.', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='specification',
            name='title_ind',
            field=models.CharField(help_text='Title of specification.', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='specification',
            name='title_ko',
            field=models.CharField(help_text='Title of specification.', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='specification',
            name='value_af',
            field=models.CharField(help_text='Value of specification.', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='specification',
            name='value_en',
            field=models.CharField(help_text='Value of specification.', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='specification',
            name='value_ind',
            field=models.CharField(help_text='Value of specification.', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='specification',
            name='value_ko',
            field=models.CharField(help_text='Value of specification.', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='worksheet',
            name='exercise_goal_af',
            field=models.CharField(help_text='The goal of the exercise.', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='worksheet',
            name='exercise_goal_en',
            field=models.CharField(help_text='The goal of the exercise.', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='worksheet',
            name='exercise_goal_ind',
            field=models.CharField(help_text='The goal of the exercise.', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='worksheet',
            name='exercise_goal_ko',
            field=models.CharField(help_text='The goal of the exercise.', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='worksheet',
            name='exercise_task_af',
            field=models.TextField(help_text='Task in the exercise.', max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='worksheet',
            name='exercise_task_en',
            field=models.TextField(help_text='Task in the exercise.', max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='worksheet',
            name='exercise_task_ind',
            field=models.TextField(help_text='Task in the exercise.', max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='worksheet',
            name='exercise_task_ko',
            field=models.TextField(help_text='Task in the exercise.', max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='worksheet',
            name='module_af',
            field=models.CharField(help_text='Name of worksheet.', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='worksheet',
            name='module_en',
            field=models.CharField(help_text='Name of worksheet.', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='worksheet',
            name='module_ind',
            field=models.CharField(help_text='Name of worksheet.', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='worksheet',
            name='module_ko',
            field=models.CharField(help_text='Name of worksheet.', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='worksheet',
            name='more_about_text_af',
            field=models.TextField(help_text='More detail about the content of the worksheet.', max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='worksheet',
            name='more_about_text_en',
            field=models.TextField(help_text='More detail about the content of the worksheet.', max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='worksheet',
            name='more_about_text_ind',
            field=models.TextField(help_text='More detail about the content of the worksheet.', max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='worksheet',
            name='more_about_text_ko',
            field=models.TextField(help_text='More detail about the content of the worksheet.', max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='worksheet',
            name='summary_leader_af',
            field=models.CharField(help_text='Title of the summary.', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='worksheet',
            name='summary_leader_en',
            field=models.CharField(help_text='Title of the summary.', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='worksheet',
            name='summary_leader_ind',
            field=models.CharField(help_text='Title of the summary.', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='worksheet',
            name='summary_leader_ko',
            field=models.CharField(help_text='Title of the summary.', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='worksheet',
            name='summary_text_af',
            field=models.TextField(help_text='Content of the summary.', max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='worksheet',
            name='summary_text_en',
            field=models.TextField(help_text='Content of the summary.', max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='worksheet',
            name='summary_text_ind',
            field=models.TextField(help_text='Content of the summary.', max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='worksheet',
            name='summary_text_ko',
            field=models.TextField(help_text='Content of the summary.', max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='worksheet',
            name='title_af',
            field=models.CharField(help_text='Title of module.', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='worksheet',
            name='title_en',
            field=models.CharField(help_text='Title of module.', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='worksheet',
            name='title_ind',
            field=models.CharField(help_text='Title of module.', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='worksheet',
            name='title_ko',
            field=models.CharField(help_text='Title of module.', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='worksheetquestion',
            name='question_af',
            field=models.CharField(help_text='Question.', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='worksheetquestion',
            name='question_en',
            field=models.CharField(help_text='Question.', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='worksheetquestion',
            name='question_ind',
            field=models.CharField(help_text='Question.', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='worksheetquestion',
            name='question_ko',
            field=models.CharField(help_text='Question.', max_length=200, null=True),
        ),
    ]
