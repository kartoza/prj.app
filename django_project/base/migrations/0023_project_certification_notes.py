# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0022_auto_20180702_0420'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='certification_notes',
            field=models.TextField(help_text='Notes about the certification programme for this project', null=True, blank=True),
        ),
    ]
