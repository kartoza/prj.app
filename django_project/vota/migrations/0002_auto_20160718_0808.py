# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import vota.models.ballot


class Migration(migrations.Migration):

    dependencies = [
        ('vota', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ballot',
            name='closes',
            field=models.DateTimeField(default=vota.models.ballot.closes_default_time, help_text='Date the ballot closes'),
        ),
    ]
