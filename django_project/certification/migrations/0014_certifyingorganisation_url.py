# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certification', '0013_auto_20171014_1045'),
    ]

    operations = [
        migrations.AddField(
            model_name='certifyingorganisation',
            name='url',
            field=models.URLField(help_text="Optional URL for the certifying organisation's home page", null=True, blank=True),
        ),
    ]
