# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certification', '0010_auto_20170817_1718'),
    ]

    operations = [
        migrations.AddField(
            model_name='certifyingorganisation',
            name='credits_certificate',
            field=models.IntegerField(default=0, help_text='Credits for issuing certificate', null=True, blank=True),
        ),
    ]
