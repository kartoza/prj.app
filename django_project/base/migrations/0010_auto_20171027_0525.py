# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_project_certification_manager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='sponsorship_programme',
            field=models.TextField(help_text='Sponsorship programme for this project. Markdown is supported', max_length=10000, null=True, blank=True),
        ),
    ]
