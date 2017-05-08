# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certification', '0002_auto_20170502_0828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certifyingorganisation',
            name='name',
            field=models.CharField(help_text=b'Name of Organisation or Institution.', unique=True, max_length=200),
        ),
    ]
