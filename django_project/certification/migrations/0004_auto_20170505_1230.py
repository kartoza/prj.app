# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certification', '0003_auto_20170505_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certifyingorganisation',
            name='address',
            field=models.TextField(help_text=b'Address of Organisation or Institution.', max_length=1000),
        ),
        migrations.AlterField(
            model_name='certifyingorganisation',
            name='organisation_phone',
            field=models.CharField(help_text=b'Phone number: (country code)(number) e.g. +6221551553', max_length=200),
        ),
    ]
