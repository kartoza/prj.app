# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings
import certification.models.certifying_organisation
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0022_auto_20180702_0420'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('certification', '0023_auto_20190904_1523'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalCertifyingOrganisation',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('name', models.CharField(help_text='Name of organisation or institution', max_length=200)),
                ('organisation_email', models.CharField(help_text='Email address organisation or institution.', max_length=200, validators=[certification.models.certifying_organisation.validate_email_address])),
                ('url', models.URLField(help_text="Optional URL for the certifying organisation's home page", null=True, blank=True)),
                ('address', models.TextField(help_text='Address of Organisation or Institution.', max_length=1000)),
                ('logo', models.TextField(help_text='Logo for this organisation. Most browsers support dragging the image directly on to the "Choose File" button above.', max_length=100, blank=True)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2, null=True, help_text='Select the country for this Institution')),
                ('organisation_phone', models.CharField(help_text='Phone number: (country code)(number) e.g. +6221551553', max_length=200)),
                ('organisation_credits', models.IntegerField(default=0, help_text='Credits available', null=True, blank=True)),
                ('approved', models.BooleanField(default=False, help_text='Approval from project admin')),
                ('enabled', models.BooleanField(default=True, help_text='Project enabled')),
                ('rejected', models.BooleanField(default=False, help_text='Rejection from project admin')),
                ('remarks', models.CharField(help_text='Remarks regarding status of this organisation, i.e. Rejected, because lacks of information', max_length=500, null=True, blank=True)),
                ('slug', models.SlugField()),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('project', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='base.Project', null=True)),
                ('status', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='certification.Status', null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical certifying organisation',
            },
        ),
    ]
