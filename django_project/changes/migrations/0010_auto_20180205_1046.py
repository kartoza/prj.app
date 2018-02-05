# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('changes', '0009_auto_20180116_1849'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entry',
            options={'ordering': ['version', 'category', 'sequence_number']},
        ),
        migrations.AddField(
            model_name='entry',
            name='sequence_number',
            field=models.IntegerField(default=0, help_text='The order in which this entry is listed within the category.', verbose_name='Entry number'),
        ),
    ]
