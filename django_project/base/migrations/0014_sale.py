# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_auto_20180103_0937'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('charge_id', models.CharField(max_length=32, null=True, verbose_name='Charge ID', blank=True)),
                ('charge_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10, blank=True, help_text='Amount charged on account in dollars', null=True, verbose_name='Charge amount')),
                ('charge_stripe_id', models.CharField(max_length=50, null=True, verbose_name='Charge stripe ID', blank=True)),
                ('merchant_stripe_id', models.CharField(max_length=50, null=True, verbose_name='Mechant stripe ID', blank=True)),
                ('customer_stripe_id', models.CharField(max_length=50, null=True, verbose_name='Customer stripe ID', blank=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, help_text='Enter the date and time when the payment was made.', verbose_name='Timestamp')),
            ],
        ),
    ]
