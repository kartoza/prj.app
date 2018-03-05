# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certification', '0015_auto_20180207_1243'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_language',
            field=models.CharField(default='English', max_length=200, null=True, help_text='A language that the Course will be conducted in,  e.g. English.', blank=True),
        ),
    ]
