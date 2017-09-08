# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certification', '0010_auto_20170817_1718'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificate',
            name='is_paid',
            field=models.BooleanField(default=False, help_text='Is this certificate paid?'),
        ),
        migrations.AddField(
            model_name='certifyingorganisation',
            name='organisation_credits',
            field=models.IntegerField(default=0, help_text='Credits available', null=True, blank=True),
        ),
    ]
