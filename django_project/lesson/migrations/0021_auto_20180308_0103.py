# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0020_auto_20180308_0056'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='last_update',
            field=models.DateTimeField(help_text='Time stamp when the last worksheet updated.', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='last_update_en',
            field=models.DateTimeField(help_text='Time stamp when the last worksheet updated.', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='last_update_ind',
            field=models.DateTimeField(help_text='Time stamp when the last worksheet updated.', null=True, blank=True),
        ),
    ]
