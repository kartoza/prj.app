# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_countries.fields
import django.contrib.gis.db.models.fields
import django.utils.timezone
from django.conf import settings
import certification.models.certifying_organisation


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_project_sponsorship_programme'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('firstname', models.CharField(help_text='First name of the attendee.', max_length=200)),
                ('surname', models.CharField(help_text='Surname of the attendee.', max_length=200)),
                ('email', models.CharField(help_text='Email address.', max_length=200, validators=[certification.models.certifying_organisation.validate_email_address])),
                ('slug', models.SlugField()),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['firstname'],
            },
        ),
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('int_id', models.AutoField(serialize=False, primary_key=True)),
                ('certificateID', models.CharField(default=b'', max_length=100, blank=True)),
                ('is_paid', models.BooleanField(default=False, help_text='Is this certificate paid?')),
                ('attendee', models.ForeignKey(to='certification.Attendee')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['certificateID'],
            },
        ),
        migrations.CreateModel(
            name='CertifyingOrganisation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='name of organisation or institution', max_length=200)),
                ('organisation_email', models.CharField(help_text='Email address organisation or institution.', max_length=200, validators=[certification.models.certifying_organisation.validate_email_address])),
                ('address', models.TextField(help_text='Address of Organisation or Institution.', max_length=1000)),
                ('logo', models.ImageField(help_text='Logo for this organisation. Most browsers support dragging the image directly on to the "Choose File" button above.', upload_to=b'images/organisations', blank=True)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2, null=True, help_text='Select the country for this Institution')),
                ('organisation_phone', models.CharField(help_text='Phone number: (country code)(number) e.g. +6221551553', max_length=200)),
                ('organisation_credits', models.IntegerField(default=0, help_text='Credits available', null=True, blank=True)),
                ('approved', models.BooleanField(default=False, help_text='Approval from project admin')),
                ('enabled', models.BooleanField(default=True, help_text='Project enabled')),
                ('slug', models.SlugField()),
                ('organisation_owners', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(to='base.Project')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Course name.', max_length=200, null=True, blank=True)),
                ('start_date', models.DateField(default=django.utils.timezone.now, help_text='Course start date', verbose_name='Start date')),
                ('end_date', models.DateField(default=django.utils.timezone.now, help_text='Course end date', verbose_name='End date')),
                ('slug', models.CharField(default=b'', max_length=400, blank=True)),
                ('template_certificate', models.ImageField(help_text='Background template of the certificate. Most browsers support dragging the image directly on to the "Choose File" button above.', upload_to=b'images/organisations/certificates', blank=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('certifying_organisation', models.ForeignKey(to='certification.CertifyingOrganisation')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='CourseAttendee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attendee', models.ForeignKey(to='certification.Attendee')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('course', models.ForeignKey(to='certification.Course')),
            ],
        ),
        migrations.CreateModel(
            name='CourseConvener',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.CharField(default=b'', max_length=100, blank=True)),
                ('signature', models.ImageField(help_text='Signature of the course convener. Most browsers support dragging the image directly on to the "Choose File" button above.', upload_to=b'images/organisations/conveners', blank=True)),
                ('certifying_organisation', models.ForeignKey(to='certification.CertifyingOrganisation')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user'],
            },
        ),
        migrations.CreateModel(
            name='CourseType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Course type.', max_length=200)),
                ('description', models.TextField(help_text='Course type description.', max_length=250, null=True, blank=True)),
                ('instruction_hours', models.CharField(help_text='Number of instruction hours e.g. 40 hours', max_length=200, null=True, blank=True)),
                ('coursetype_link', models.CharField(help_text=b'Link to course types e.g. http://kartoza.com/', max_length=200, null=True, verbose_name=b'Link', blank=True)),
                ('slug', models.SlugField(unique=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('certifying_organisation', models.ForeignKey(to='certification.CertifyingOrganisation')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='TrainingCenter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Training Center name.', unique=True, max_length=150)),
                ('email', models.CharField(help_text='Valid email address for communication purposes.', max_length=150, validators=[certification.models.certifying_organisation.validate_email_address])),
                ('address', models.TextField(help_text='Address of the training center.', max_length=250)),
                ('phone', models.CharField(help_text='Phone number: (country code)(number) e.g. +6221551553', max_length=150)),
                ('location', django.contrib.gis.db.models.fields.GeometryField(srid=4326, null=True, blank=True)),
                ('slug', models.SlugField()),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('certifying_organisation', models.ForeignKey(to='certification.CertifyingOrganisation')),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(certification.models.certifying_organisation.SlugifyingMixin, models.Model),
        ),
        migrations.AddField(
            model_name='course',
            name='course_convener',
            field=models.ForeignKey(to='certification.CourseConvener'),
        ),
        migrations.AddField(
            model_name='course',
            name='course_type',
            field=models.ForeignKey(to='certification.CourseType'),
        ),
        migrations.AddField(
            model_name='course',
            name='training_center',
            field=models.ForeignKey(to='certification.TrainingCenter'),
        ),
        migrations.AddField(
            model_name='certificate',
            name='course',
            field=models.ForeignKey(to='certification.Course'),
        ),
        migrations.AddField(
            model_name='attendee',
            name='certifying_organisation',
            field=models.ForeignKey(to='certification.CertifyingOrganisation', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='coursetype',
            unique_together=set([('name', 'certifying_organisation')]),
        ),
        migrations.AlterUniqueTogether(
            name='courseattendee',
            unique_together=set([('attendee', 'course')]),
        ),
        migrations.AlterUniqueTogether(
            name='course',
            unique_together=set([('course_convener', 'course_type', 'training_center', 'start_date', 'end_date', 'certifying_organisation')]),
        ),
        migrations.AlterUniqueTogether(
            name='certifyingorganisation',
            unique_together=set([('name', 'project')]),
        ),
        migrations.AlterUniqueTogether(
            name='certificate',
            unique_together=set([('course', 'attendee', 'certificateID')]),
        ),
        migrations.AlterUniqueTogether(
            name='attendee',
            unique_together=set([('firstname', 'surname', 'email', 'certifying_organisation')]),
        ),
    ]
