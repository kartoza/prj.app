# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certification', '0022_auto_20190904_1205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certifyingorganisation',
            name='status',
            field=models.ForeignKey(blank=True, to='certification.Status', null=True),
        ),
    ]
