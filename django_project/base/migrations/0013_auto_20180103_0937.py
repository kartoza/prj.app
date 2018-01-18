# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings
import base.models.project


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0012_project_sponsorship_manager'),
    ]

    operations = [
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(default=b'project', help_text='For organisation, domain will point to list of projects within the organisation and for project, domain will only point to a specific project.', max_length=30, choices=[(b'Project', b'Project'), (b'Organisation', b'Organisation')])),
                ('domain', models.CharField(help_text='Custom domain, i.e. projecta.kartoza.com.', unique=True, max_length=30)),
                ('approved', models.BooleanField(default=False, help_text='Whether this domain has been approved for use yet.')),
                ('paid', models.BooleanField(default=False, help_text='Whether this domain has been paid for use yet.')),
            ],
            options={
                'ordering': ['domain'],
            },
        ),
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Name of this organisation.', unique=True, max_length=150)),
                ('approved', models.BooleanField(default=False, help_text='Whether this organisation has been approved for use yet.')),
                ('owner', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='domain',
            name='organisation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='base.Organisation', null=True),
        ),
        migrations.AddField(
            model_name='domain',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='base.Project', null=True),
        ),
        migrations.AddField(
            model_name='domain',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='project',
            name='organisation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_DEFAULT, default=base.models.project.get_default_organisation, to='base.Organisation', null=True),
        ),
    ]
