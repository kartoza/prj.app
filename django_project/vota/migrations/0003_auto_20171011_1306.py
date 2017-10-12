# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('vota', '0002_auto_20171011_1305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ballot',
            name='closes',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 18, 11, 6, 9, 351398, tzinfo=utc), help_text='Date the ballot closes'),
        ),
    ]
