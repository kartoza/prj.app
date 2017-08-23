# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certification', '0009_auto_20170710_0708'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificate',
            name='cost',
            field=models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True),
        ),
        migrations.AddField(
            model_name='certificate',
            name='is_paid',
            field=models.BooleanField(default=False, help_text='Has certificate been paid?'),
        ),
        migrations.AddField(
            model_name='certificate',
            name='transaction_id',
            field=models.CharField(help_text='Transaction ID', max_length=250, blank=True),
        ),
    ]
