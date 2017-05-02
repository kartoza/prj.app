# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import certification.models.certifying_organisation


class Migration(migrations.Migration):

    dependencies = [
        ('certification', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certifyingorganisation',
            name='organisation_email',
            field=models.CharField(help_text=b'Email address Organisation or Institution.', max_length=200, validators=[certification.models.certifying_organisation.validate_email_address]),
        ),
    ]
