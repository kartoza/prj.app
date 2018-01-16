# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('changes', '0009_sponsor_sponsorship_contact_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsor',
            name='sponsor_invoice_number',
            field=models.CharField(help_text='Invoice number for the sponsor.', max_length=255, null=True, verbose_name='Sponsorship invoice number', blank=True),
        ),
    ]
