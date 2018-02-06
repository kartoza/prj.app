# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0016_auto_20180201_1642'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lesson', '0015_auto_20180201_1607'),
    ]

    operations = [
        migrations.CreateModel(
            name='Curriculum',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text='Title of the curriculum.', max_length=200, verbose_name='Title of the curriculum')),
                ('competency', models.CharField(help_text='Competency.', max_length=200, null=True, verbose_name='Competency', blank=True)),
                ('presenter_logo', models.ImageField(help_text='Presenter logo. Most browsers support dragging the image directly on to the "Choose File" button above.', upload_to=b'images/lesson/curriculum/presenter', blank=True)),
                ('slug', models.SlugField()),
                ('owner', models.ForeignKey(help_text='The owner of the curriculum.', to=settings.AUTH_USER_MODEL)),
                ('presenters', models.ManyToManyField(help_text='Users who are presenting this curriculum.', related_name='presenters', to=settings.AUTH_USER_MODEL, blank=True)),
                ('project', models.ForeignKey(verbose_name='Project name', to='base.Project', help_text='The project.')),
            ],
            options={
                'ordering': ['project', 'title'],
            },
        ),
        migrations.CreateModel(
            name='CurriculumWorksheets',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sequence_number', models.IntegerField(default=0, help_text='The order in which this worksheet is listed within a curriculum', verbose_name='Worksheet number')),
                ('curriculum', models.ForeignKey(to='lesson.Curriculum')),
                ('worksheet', models.ForeignKey(to='lesson.Worksheet')),
            ],
        ),
    ]
