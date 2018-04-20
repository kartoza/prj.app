# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certification', '0018_auto_20180328_1302'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='certificate',
            unique_together=set([('course', 'attendee')]),
        ),
    ]
