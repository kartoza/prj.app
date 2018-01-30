# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0002_auto_20180117_0335'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='section',
            unique_together=set([('slug', 'project')]),
        ),
    ]
