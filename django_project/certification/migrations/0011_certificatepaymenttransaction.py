# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('certification', '0010_auto_20170723_1604'),
    ]

    operations = [
        migrations.CreateModel(
            name='CertificatePaymentTransaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('transaction_date', models.DateField(default=django.utils.timezone.now, help_text='Date of the transaction', verbose_name='Transaction Date')),
                ('amount', models.DecimalField(max_digits=10, decimal_places=2)),
                ('certificate', models.ManyToManyField(to='certification.Certificate')),
                ('certifying_organisation', models.ForeignKey(to='certification.CertifyingOrganisation')),
            ],
            options={
                'ordering': ['transaction_date'],
            },
        ),
    ]
