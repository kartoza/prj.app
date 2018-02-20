# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0016_auto_20180201_1642'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='certification_manager',
            new_name='certification_managers',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='changelog_manager',
            new_name='changelog_managers',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='lesson_manager',
            new_name='lesson_managers',
        ),
        migrations.RenameField(
            model_name='project',
            old_name='sponsorship_manager',
            new_name='sponsorship_managers',
        ),
        migrations.AlterField(
            model_name='project',
            name='sponsorship_programme',
            field=models.TextField(help_text='Please describe the sponsorship programme for this project (if any). Markdown is supported', max_length=10000, null=True, blank=True),
        ),
    ]
