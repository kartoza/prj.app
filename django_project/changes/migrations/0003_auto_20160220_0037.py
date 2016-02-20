# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('changes', '0002_version_release_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsor',
            name='address',
            field=models.TextField(help_text=b'Enter the complete street address for this sponsor. Use line breaks to separate address elements and use the country field to specify the country.', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='sponsor',
            name='country',
            field=django_countries.fields.CountryField(blank=True, max_length=2, null=True, help_text=b'Select the country for this sponsor'),
        ),
        migrations.AlterField(
            model_name='version',
            name='release_date',
            field=models.DateField(help_text=b'Date of official release', null=True, verbose_name='Release date (yyyy-mm-dd)', blank=True),
        ),
    ]
