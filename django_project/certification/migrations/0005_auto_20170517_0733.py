# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import certification.models.certifying_organisation


class Migration(migrations.Migration):

    dependencies = [
        ('certification', '0004_auto_20170505_1230'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='slug',
            field=models.CharField(default=b'', max_length=400, blank=True),
        ),
        migrations.AlterField(
            model_name='certifyingorganisation',
            name='name',
            field=models.CharField(help_text='name of organisation or institution', unique=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='certifyingorganisation',
            name='organisation_email',
            field=models.CharField(help_text='Email address organisation or institution.', max_length=200, validators=[certification.models.certifying_organisation.validate_email_address]),
        ),
        migrations.AlterField(
            model_name='coursetype',
            name='coursetype_link',
            field=models.CharField(help_text=b'Link to course types e.g. http://kartoza.com/', max_length=200, null=True, verbose_name=b'Link', blank=True),
        ),
        migrations.AlterField(
            model_name='trainingcenter',
            name='address',
            field=models.TextField(help_text='Address of the training center.', max_length=250),
        ),
        migrations.AlterField(
            model_name='trainingcenter',
            name='email',
            field=models.CharField(help_text='Valid email address for communication purposes.', max_length=150, validators=[certification.models.certifying_organisation.validate_email_address]),
        ),
        migrations.AlterField(
            model_name='trainingcenter',
            name='name',
            field=models.CharField(help_text='Training Center name.', unique=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='trainingcenter',
            name='phone',
            field=models.CharField(help_text='Phone number: (country code)(number) e.g. +6221551553', max_length=150),
        ),
    ]
