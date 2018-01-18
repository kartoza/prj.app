# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('changes', '0007_auto_20170922_1040'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sponsor',
            options={'ordering': ['project', 'name']},
        ),
        migrations.AlterModelOptions(
            name='sponsorshiplevel',
            options={'ordering': ['project', '-value']},
        ),
        migrations.AlterModelOptions(
            name='sponsorshipperiod',
            options={'ordering': ['project', '-end_date']},
        ),
    ]
