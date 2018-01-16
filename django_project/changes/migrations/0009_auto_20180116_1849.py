# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import changes.models.sponsor


class Migration(migrations.Migration):

    dependencies = [
        ('changes', '0008_auto_20180110_1054'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsor',
            name='contact_title',
            field=models.CharField(help_text='Title of the sponsorship representative i.e Treasurer.', max_length=255, null=True, verbose_name='Sponsorship Representative Title', blank=True),
        ),
        migrations.AddField(
            model_name='sponsor',
            name='invoice_number',
            field=models.CharField(help_text='Invoice number for the sponsor.', max_length=255, null=True, verbose_name='Sponsorship invoice number', blank=True),
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='sponsor_email',
            field=models.CharField(blank=True, max_length=255, null=True, help_text=b'Input an email of sponsor.', validators=[changes.models.sponsor.validate_email_address]),
        ),
    ]
