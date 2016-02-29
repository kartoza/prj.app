# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('changes', '0004_auto_20160221_2103'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsorshiplevel',
            name='logo_height',
            field=models.IntegerField(default=100, help_text=b'Enter the height of the icon that should be used on the changelog'),
        ),
        migrations.AddField(
            model_name='sponsorshiplevel',
            name='logo_width',
            field=models.IntegerField(default=100, help_text=b'Enter the width of the icon that should be used on the changelog'),
        ),
    ]
