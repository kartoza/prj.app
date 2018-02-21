# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0018_auto_20180220_0339'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='project_repository_url',
            field=models.URLField(help_text='A repository url for this project i.e github repository url', null=True, blank=True),
        ),
    ]
