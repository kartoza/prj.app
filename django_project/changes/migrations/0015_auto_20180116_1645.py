# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import changes.models.sponsor


class Migration(migrations.Migration):

    dependencies = [
        ('changes', '0014_auto_20180109_1728'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sponsor',
            old_name='sponsorship_contact_title',
            new_name='contact_title',
        ),
        migrations.RenameField(
            model_name='sponsor',
            old_name='sponsor_invoice_number',
            new_name='invoice_number',
        ),
        migrations.RemoveField(
            model_name='sponsor',
            name='sponsorship_contact_email',
        ),
        migrations.RemoveField(
            model_name='sponsor',
            name='sponsorship_contact_name',
        ),
        migrations.RemoveField(
            model_name='sponsor',
            name='sponsorship_office_address',
        ),
        migrations.AlterField(
            model_name='sponsor',
            name='sponsor_email',
            field=models.CharField(blank=True, max_length=255, null=True, help_text=b'Input an email of sponsor.', validators=[changes.models.sponsor.validate_email_address]),
        ),
    ]
