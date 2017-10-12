# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('vota', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ballot',
            name='closes',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 18, 11, 5, 12, 115519, tzinfo=utc), help_text='Date the ballot closes'),
        ),
    ]
