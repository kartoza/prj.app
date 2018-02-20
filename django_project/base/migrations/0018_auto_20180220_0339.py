# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0017_auto_20180220_0333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='certification_managers',
            field=models.ManyToManyField(help_text='Managers of the certification app in this project. They will receive email notification about organisation and have the same permissions as project owner in the certification app.', related_name='certification_managers', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='changelog_managers',
            field=models.ManyToManyField(help_text='Managers of the changelog in this project. They will be allowed to approve changelog entries in the moderation queue.', related_name='changelog_managers', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='lesson_managers',
            field=models.ManyToManyField(help_text='Managers of the lesson app in this project. They will be allowed to create or remove lessons.', related_name='lesson_managers', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='sponsorship_managers',
            field=models.ManyToManyField(help_text='Managers of the sponsorship in this project. They will be allowed to approve sponsor entries in the moderation queue.', related_name='sponsorship_managers', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
