# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certification', '0014_certifyingorganisation_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursetype',
            name='description',
            field=models.TextField(help_text='Course type description - 1000 characters limit.', max_length=1000, null=True, blank=True),
        ),
    ]
