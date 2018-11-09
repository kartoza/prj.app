# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('changes', '0013_remove_entry_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='version',
            name='locked',
            field=models.BooleanField(default=False, help_text=b'Whether this version is locked for editing.'),
        ),
    ]
