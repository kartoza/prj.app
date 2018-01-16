# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('changes', '0010_sponsor_sponsor_invoice_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsor',
            name='sponsorship_representative',
            field=models.CharField(help_text='Name of the sponsorship representative.', max_length=255, null=True, verbose_name='Sponsorship Representative', blank=True),
        ),
        migrations.AddField(
            model_name='sponsor',
            name='sposnorship_representative_title',
            field=models.CharField(help_text='Title of the sponsorship representative i.e Treasurer.', max_length=255, null=True, verbose_name='Sponsorship Representative Title', blank=True),
        ),
    ]
