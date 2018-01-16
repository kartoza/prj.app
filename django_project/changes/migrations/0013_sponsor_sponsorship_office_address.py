# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('changes', '0012_auto_20180109_1718'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsor',
            name='sponsorship_office_address',
            field=models.TextField(help_text=b'Enter the complete address for the sponsorship office. Use line breaks to separate address elements', null=True, blank=True),
        ),
    ]
