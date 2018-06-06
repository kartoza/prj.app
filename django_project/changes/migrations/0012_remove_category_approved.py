# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('changes', '0011_remove_version_approved'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='approved',
        ),
    ]
