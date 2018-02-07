# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0016_curriculum_curriculumworksheets'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curriculum',
            name='slug',
            field=models.SlugField(unique=True),
        ),
        migrations.AlterField(
            model_name='section',
            name='slug',
            field=models.SlugField(unique=True),
        ),
        migrations.AlterField(
            model_name='worksheet',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
