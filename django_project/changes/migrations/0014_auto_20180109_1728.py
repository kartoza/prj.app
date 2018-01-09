# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('changes', '0013_sponsor_sponsorship_office_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sponsor',
            old_name='sposnorship_contact_title',
            new_name='sponsorship_contact_title',
        ),
    ]
