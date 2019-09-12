# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('certification', '0024_historicalcertifyingorganisation'),
    ]

    operations = [
        migrations.CreateModel(
            name='CertifyingOrganisationCertificate',
            fields=[
                ('int_id', models.AutoField(serialize=False, primary_key=True)),
                ('certificateID', models.CharField(default=b'', max_length=100, blank=True)),
                ('issued', models.DateTimeField(default=datetime.datetime(2019, 9, 12, 4, 41, 11, 444179))),
                ('valid', models.BooleanField(default=True, help_text='Is this certificate still valid?')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('certifying_organisation', models.ForeignKey(to='certification.CertifyingOrganisation')),
            ],
            options={
                'ordering': ['certificateID'],
            },
        ),
        migrations.CreateModel(
            name='HistoricalCertifyingOrganisationCertificate',
            fields=[
                ('int_id', models.IntegerField(db_index=True, blank=True)),
                ('certificateID', models.CharField(default=b'', max_length=100, blank=True)),
                ('issued', models.DateTimeField(default=datetime.datetime(2019, 9, 12, 4, 41, 11, 444179))),
                ('valid', models.BooleanField(default=True, help_text='Is this certificate still valid?')),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('author', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('certifying_organisation', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='certification.CertifyingOrganisation', null=True)),
                ('history_user', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical certifying organisation certificate',
            },
        ),
    ]
