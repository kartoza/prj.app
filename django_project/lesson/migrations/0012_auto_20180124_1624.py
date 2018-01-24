# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0011_auto_20180123_1406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='answer_explanation',
            field=models.TextField(help_text='Answer explanation. Markdown is supported.', max_length=1000, blank=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='answer_explanation_en',
            field=models.TextField(help_text='Answer explanation. Markdown is supported.', max_length=1000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='answer_explanation_ind',
            field=models.TextField(help_text='Answer explanation. Markdown is supported.', max_length=1000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='section',
            name='notes',
            field=models.TextField(help_text='Section notes.', max_length=1000, verbose_name='Section notes. Markdown is supported.'),
        ),
        migrations.AlterField(
            model_name='section',
            name='notes_en',
            field=models.TextField(help_text='Section notes.', max_length=1000, null=True, verbose_name='Section notes. Markdown is supported.'),
        ),
        migrations.AlterField(
            model_name='section',
            name='notes_ind',
            field=models.TextField(help_text='Section notes.', max_length=1000, null=True, verbose_name='Section notes. Markdown is supported.'),
        ),
        migrations.AlterField(
            model_name='worksheet',
            name='exercise_task',
            field=models.TextField(help_text='Task in the exercise. Markdown is supported.', max_length=1000),
        ),
        migrations.AlterField(
            model_name='worksheet',
            name='exercise_task_en',
            field=models.TextField(help_text='Task in the exercise. Markdown is supported.', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='worksheet',
            name='exercise_task_ind',
            field=models.TextField(help_text='Task in the exercise. Markdown is supported.', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='worksheet',
            name='more_about_text',
            field=models.TextField(help_text='More detail about the content of the worksheet. Markdown is supported.', max_length=2000),
        ),
        migrations.AlterField(
            model_name='worksheet',
            name='more_about_text_en',
            field=models.TextField(help_text='More detail about the content of the worksheet. Markdown is supported.', max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='worksheet',
            name='more_about_text_ind',
            field=models.TextField(help_text='More detail about the content of the worksheet. Markdown is supported.', max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='worksheet',
            name='more_about_title',
            field=models.CharField(default='More about', help_text='More about title.', max_length=200),
        ),
        migrations.AlterField(
            model_name='worksheet',
            name='summary_image',
            field=models.ImageField(help_text='Image of the summary. A landscape image, approximately 800*200. Most browsers support dragging the image directly on to the "Choose File" button above.', upload_to=b'images/lesson/worksheet/summary_image', blank=True),
        ),
        migrations.AlterField(
            model_name='worksheet',
            name='summary_text',
            field=models.TextField(help_text='Content of the summary. Markdown is supported.', max_length=1000),
        ),
        migrations.AlterField(
            model_name='worksheet',
            name='summary_text_en',
            field=models.TextField(help_text='Content of the summary. Markdown is supported.', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='worksheet',
            name='summary_text_ind',
            field=models.TextField(help_text='Content of the summary. Markdown is supported.', max_length=1000, null=True),
        ),
    ]
