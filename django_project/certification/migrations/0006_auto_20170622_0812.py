# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import certification.models.certifying_organisation


class Migration(migrations.Migration):

    dependencies = [
        ('certification', '0005_auto_20170517_0733'),
    ]

    operations = [
        migrations.AddField(
            model_name='certifyingorganisation',
            name='logo',
            field=models.ImageField(help_text='Logo for this organisation. Most browsers support dragging the image directly on to the "Choose File" button above.', upload_to=b'images/organisations', blank=True),
        ),
        migrations.AddField(
            model_name='courseconvener',
            name='signature',
            field=models.ImageField(help_text='Signature of the course convener. Most browsers support dragging the image directly on to the "Choose File" button above.', upload_to=b'images/organisations/conveners', blank=True),
        ),
        migrations.AlterField(
            model_name='attendee',
            name='email',
            field=models.CharField(help_text='Email address.', max_length=200, validators=[certification.models.certifying_organisation.validate_email_address]),
        ),
        migrations.AlterField(
            model_name='attendee',
            name='firstname',
            field=models.CharField(help_text='First name of the attendee.', max_length=200),
        ),
        migrations.AlterField(
            model_name='attendee',
            name='surname',
            field=models.CharField(help_text='Surname of the attendee.', max_length=200),
        ),
    ]
