# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0012_auto_20180124_1624'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='worksheetquestion',
            options={'ordering': ['worksheet', 'sequence_number']},
        ),
        migrations.AlterUniqueTogether(
            name='worksheetquestion',
            unique_together=set([('worksheet', 'sequence_number')]),
        ),
    ]
