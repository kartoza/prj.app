# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('changes', '0010_auto_20180205_1046'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='version',
            name='approved',
        ),
    ]
