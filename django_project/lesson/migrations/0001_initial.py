# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_auto_20180103_0937'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer_number', models.IntegerField(help_text='Answer number.')),
                ('is_correct', models.BooleanField(help_text='Is this answer correct?')),
                ('answer', models.CharField(help_text='Answer.', max_length=200)),
                ('answer_explanation', models.TextField(help_text='Answer explanation.', max_length=1000, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='FurtherReading',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(help_text='Text of the further reading.', max_length=200)),
                ('link', models.CharField(help_text='Further reading link.', max_length=200, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('section_number', models.IntegerField(help_text='Section number.', unique=True, verbose_name='Section number')),
                ('name', models.CharField(help_text='Name of section.', max_length=200, verbose_name='Name of section')),
                ('notes', models.TextField(help_text='Section notes.', max_length=1000, verbose_name='Section notes.')),
                ('slug', models.SlugField()),
                ('project', models.ForeignKey(verbose_name='Project name', to='base.Project')),
            ],
            options={
                'ordering': ['section_number'],
            },
        ),
        migrations.CreateModel(
            name='Specification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('specification_number', models.IntegerField(help_text='Used to order the specifications for a lesson into the correct sequence.')),
                ('title', models.CharField(help_text='Title of specification.', max_length=200)),
                ('value', models.CharField(help_text='Value of specification.', max_length=200)),
                ('notes', models.CharField(help_text='Notes of specification.', max_length=200, blank=True)),
            ],
            options={
                'ordering': ['specification_number'],
            },
        ),
        migrations.CreateModel(
            name='Worksheet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('module', models.CharField(help_text='Name of worksheet.', max_length=200)),
                ('title', models.CharField(help_text='Title of module.', max_length=200)),
                ('summary_leader', models.CharField(help_text='Title of the summary.', max_length=200)),
                ('summary_text', models.TextField(help_text='Content of the summary.', max_length=1000)),
                ('summary_image', models.ImageField(help_text='Image of the summary. Most browsers support dragging the image directly on to the "Choose File" button above.', upload_to=b'images/lesson/worksheet/summary_image', blank=True)),
                ('exercise_goal', models.CharField(help_text='The goal of the exercise.', max_length=200)),
                ('exercise_task', models.TextField(help_text='Task in the exercise.', max_length=1000)),
                ('more_about_text', models.TextField(help_text='More detail about the content of the worksheet.', max_length=2000)),
                ('more_about_image', models.ImageField(help_text='Image for the more about part. Most browsers support dragging the image directly on to the "Choose File" button above.', upload_to=b'images/lesson/worksheet/more_about', blank=True)),
                ('section', models.ForeignKey(to='lesson.Section')),
            ],
            options={
                'ordering': ['module'],
            },
        ),
        migrations.CreateModel(
            name='WorksheetQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.CharField(help_text='Question.', max_length=200)),
                ('question_number', models.IntegerField(help_text='Question number.')),
                ('question_image', models.ImageField(help_text='Image for the question. Most browsers support dragging the image directly on to the "Choose File" button above.', upload_to=b'images/lesson/worksheet_question/question_image', blank=True)),
                ('worksheet', models.ForeignKey(to='lesson.Worksheet')),
            ],
            options={
                'ordering': ['question_number', 'worksheet'],
            },
        ),
        migrations.AddField(
            model_name='specification',
            name='worksheet',
            field=models.ForeignKey(to='lesson.Worksheet'),
        ),
        migrations.AddField(
            model_name='furtherreading',
            name='worksheet',
            field=models.ForeignKey(to='lesson.Worksheet'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(to='lesson.WorksheetQuestion'),
        ),
        migrations.AlterUniqueTogether(
            name='worksheetquestion',
            unique_together=set([('question_number', 'question')]),
        ),
        migrations.AlterUniqueTogether(
            name='specification',
            unique_together=set([('specification_number', 'worksheet')]),
        ),
        migrations.AlterUniqueTogether(
            name='section',
            unique_together=set([('section_number', 'project')]),
        ),
        migrations.AlterUniqueTogether(
            name='answer',
            unique_together=set([('answer_number', 'question')]),
        ),
    ]
