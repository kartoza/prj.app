# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('changes', '0011_auto_20180109_1712'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sponsor',
            old_name='sposnorship_representative_title',
            new_name='sposnorship_contact_title',
        ),
        migrations.RemoveField(
            model_name='sponsor',
            name='sponsorship_representative',
        ),
    ]
