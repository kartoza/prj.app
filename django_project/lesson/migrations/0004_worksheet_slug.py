# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0003_auto_20180117_0349'),
    ]

    operations = [
        migrations.AddField(
            model_name='worksheet',
            name='slug',
            field=models.SlugField(default=datetime.datetime(2018, 1, 17, 9, 9, 29, 345174, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
