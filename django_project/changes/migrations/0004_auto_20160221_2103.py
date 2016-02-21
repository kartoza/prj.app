# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('changes', '0003_auto_20160220_0037'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sponsorshipperiod',
            old_name='sponsorshiplevel',
            new_name='sponsorship_level',
        ),
    ]
