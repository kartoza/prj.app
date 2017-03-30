# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certification', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='trainingcenter',
            unique_together=set([('name', 'certifying_organisation', 'project'), ('certifying_organisation', 'slug')]),
        ),
    ]
