# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certification', '0019_auto_20180420_1205'),
    ]

    operations = [
        migrations.AddField(
            model_name='certifyingorganisation',
            name='rejected',
            field=models.BooleanField(default=False, help_text='Rejection from project admin'),
        ),
        migrations.AddField(
            model_name='certifyingorganisation',
            name='status',
            field=models.CharField(help_text='Status of this organisation, i.e. Rejected, because lacks of information', max_length=500, null=True, blank=True),
        ),
    ]
