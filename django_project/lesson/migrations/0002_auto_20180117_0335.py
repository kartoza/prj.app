# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='section_number',
            field=models.IntegerField(default=0, help_text='The order in which this section is listed within a project', verbose_name='Section number'),
        ),
    ]
