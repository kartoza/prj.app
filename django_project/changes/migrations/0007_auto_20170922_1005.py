# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('changes', '0006_auto_20160718_0804'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsorshipperiod',
            name='amount_paid',
            field=models.DecimalField(decimal_places=2, max_digits=30, blank=True, help_text='The sponsorship amount that was paid for this period.', null=True, verbose_name='Amount Paid'),
        ),
        migrations.AddField(
            model_name='sponsorshipperiod',
            name='currency',
            field=models.CharField(help_text='The currency used for sponsorship payment.', max_length=50, null=True, blank=True),
        ),
    ]
