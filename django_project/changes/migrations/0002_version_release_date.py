# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('changes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='version',
            name='release_date',
            field=models.DateField(help_text=b'Date of official release', null=True, verbose_name='End date', blank=True),
        ),
    ]
