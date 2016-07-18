# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('changes', '0005_auto_20160229_2050'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sponsorshipperiod',
            options={'ordering': ['-end_date']},
        ),
    ]
