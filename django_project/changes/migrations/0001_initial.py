# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import embed_video.fields
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Name of this category.', max_length=255)),
                ('approved', models.BooleanField(default=False, help_text='Whether this version has been approved for use by the project owner.')),
                ('sort_number', models.SmallIntegerField(default=0, help_text=b'The order in which this category is listed within a project')),
                ('slug', models.SlugField()),
                ('project', models.ForeignKey(to='base.Project')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text=b'Feature title for this changelog entry.', unique=True, max_length=255)),
                ('description', models.TextField(help_text=b'Describe the new feature. Markdown is supported.', null=True, blank=True)),
                ('image_file', models.ImageField(help_text=b'A image that is related to this visual changelog entry. Most browsers support dragging the image directly on to the "Choose File" button above.', upload_to=b'images/entries', blank=True)),
                ('image_credits', models.CharField(help_text=b'Who should be credited for this image?', max_length=255, null=True, blank=True)),
                ('video', embed_video.fields.EmbedVideoField(help_text=b'Paste your youtube video link', null=True, verbose_name=b'Youtube video', blank=True)),
                ('funded_by', models.CharField(help_text=b'Input the funder name.', max_length=255, null=True, blank=True)),
                ('funder_url', models.CharField(help_text=b'Input the funder URL.', max_length=255, null=True, blank=True)),
                ('developed_by', models.CharField(help_text=b'Input the developer name.', max_length=255, null=True, blank=True)),
                ('developer_url', models.CharField(help_text=b'Input the developer URL.', max_length=255, null=True, blank=True)),
                ('approved', models.BooleanField(default=False, help_text=b'Whether this entry has been approved for use by the project owner.')),
                ('slug', models.SlugField()),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(to='changes.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Name of sponsor.', max_length=255)),
                ('sponsor_url', models.CharField(help_text=b'Input the sponsor URL.', max_length=255, null=True, blank=True)),
                ('contact_person', models.CharField(help_text=b'Input the contact person of sponsor.', max_length=255, null=True, blank=True)),
                ('sponsor_email', models.CharField(help_text=b'Input an email of sponsor.', max_length=255, null=True, blank=True)),
                ('sponsor_duration', models.CharField(help_text=b'Input the sponsor duration (in months).', max_length=20, null=True, blank=True)),
                ('start_date', models.DateTimeField(default=datetime.datetime(2015, 11, 13, 17, 9, 38, 461208), verbose_name='Start date')),
                ('end_date', models.DateTimeField(default=datetime.datetime(2015, 11, 13, 17, 9, 38, 461300), verbose_name='End date')),
                ('agreement', models.FileField(help_text=b'Attach sponsor agreement', upload_to=b'docs', blank=True)),
                ('logo', models.ImageField(help_text=b'An image of sponsor logo e.g. a splashscreen. Most browsers support dragging the image directly on to the "Choose File" button above.', upload_to=b'images/projects')),
                ('approved', models.BooleanField(default=False, help_text='Whether this sponsor has been approved for use by the project owner.')),
                ('slug', models.SlugField()),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(to='base.Project')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='SponsorshipLevel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Name of sponsorship level.', max_length=255)),
                ('logo', models.ImageField(help_text=b'An image of sponsorship level logo e.g. a bronze medal.Most browsers support dragging the image directly on to the "Choose File" button above.', upload_to=b'images/projects')),
            ],
        ),
        migrations.CreateModel(
            name='SponsorshipPeriod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField(default=datetime.date(2015, 11, 13), verbose_name='Start date')),
                ('end_date', models.DateField(default=datetime.date(2015, 11, 13), verbose_name='End date')),
                ('sponsor', models.ForeignKey(to='changes.Sponsor')),
            ],
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Name of this release e.g. 1.0.1.', max_length=255)),
                ('padded_version', models.CharField(help_text=b'Numeric version for this release e.g. 001000001 for 1.0.1 calculated by zero padding each component of maj/minor/bugfix elements from name.', max_length=9, blank=True)),
                ('approved', models.BooleanField(default=False, help_text=b'Whether this version has been approved for use by the project owner.')),
                ('image_file', models.ImageField(help_text=b'An optional image for this version e.g. a splashscreen. Most browsers support dragging the image directly on to the "Choose File" button above.', upload_to=b'images/projects', blank=True)),
                ('description', models.TextField(help_text=b'Describe the new version. Markdown is supported.', null=True, blank=True)),
                ('slug', models.SlugField()),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(to='base.Project')),
            ],
        ),
        migrations.AddField(
            model_name='sponsor',
            name='sponsorshiplevel',
            field=models.ForeignKey(to='changes.SponsorshipLevel'),
        ),
        migrations.AddField(
            model_name='entry',
            name='version',
            field=models.ForeignKey(to='changes.Version'),
        ),
        migrations.AlterUniqueTogether(
            name='version',
            unique_together=set([('slug', 'project'), ('name', 'project')]),
        ),
        migrations.AlterUniqueTogether(
            name='sponsor',
            unique_together=set([('project', 'slug'), ('name', 'project')]),
        ),
        migrations.AlterUniqueTogether(
            name='entry',
            unique_together=set([('title', 'version', 'category'), ('version', 'slug')]),
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together=set([('project', 'slug'), ('name', 'project')]),
        ),
    ]
