# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django_countries.fields
import django.utils.timezone
from django.conf import settings
import certification.models.certifying_organisation


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0002_project_gitter_room'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('firstname', models.CharField(help_text=b'First name course attendee.', max_length=200)),
                ('surname', models.CharField(help_text=b'Surname course attendee.', max_length=200)),
                ('email', models.CharField(help_text=b'Email address.', max_length=200)),
                ('slug', models.SlugField()),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['firstname'],
            },
        ),
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('certificateID', models.CharField(help_text=b'Id certificate.', max_length=200)),
                ('slug', models.SlugField()),
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
                ('name', models.CharField(help_text=b'Name of Organisation or Institution.', max_length=200)),
                ('organisation_email', models.CharField(help_text=b'Email address Organisation or Institution.', max_length=200)),
                ('address', models.CharField(help_text=b'Contact of Organisation or Institution.', max_length=200)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2, null=True, help_text=b'Select the country for this sponsor')),
                ('organisation_phone', models.CharField(help_text=b'Contact of Organisation or Institution.', max_length=200)),
                ('approved', models.BooleanField(default=False, help_text=b'Approval from project admin')),
                ('slug', models.SlugField()),
                ('organisation_manager', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(to='base.Project')),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(certification.models.certifying_organisation.SlugifyingMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Course name.', max_length=200)),
                ('start_date', models.DateField(default=django.utils.timezone.now, help_text=b'Course start date', verbose_name='Start date')),
                ('end_date', models.DateField(default=django.utils.timezone.now, help_text=b'Course end date', verbose_name='End date')),
                ('slug', models.SlugField()),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('certifying_organisation', models.ForeignKey(to='certification.CertifyingOrganisation')),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(certification.models.certifying_organisation.SlugifyingMixin, models.Model),
        ),
        migrations.CreateModel(
            name='CourseAttendee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Course attendee.', max_length=200)),
                ('slug', models.SlugField()),
                ('attendee', models.ManyToManyField(to='certification.Attendee')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('course', models.ForeignKey(to='certification.Course')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='CourseConvener',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField()),
                ('certifying_organisation', models.ForeignKey(to='certification.CertifyingOrganisation')),
                ('name', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='CourseType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Course type.', max_length=200)),
                ('descriptions', models.TextField(help_text=b'Course type descriptions.', max_length=250, null=True, blank=True)),
                ('instruction_hours', models.CharField(help_text=b'Number of instruction hours e.g. 40 hours', max_length=200, null=True, blank=True)),
                ('coursetype_link', models.CharField(help_text=b'Link to course types', max_length=200, null=True, blank=True)),
                ('slug', models.SlugField(unique=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('certifying_organisation', models.ForeignKey(to='certification.CertifyingOrganisation')),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(certification.models.certifying_organisation.SlugifyingMixin, models.Model),
        ),
        migrations.CreateModel(
            name='TrainingCenter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Organisation/Institution name.', unique=True, max_length=150)),
                ('email', models.CharField(help_text='Valid email address for communication purpose.', max_length=150)),
                ('address', models.TextField(help_text='Address of the organisation/institution.', max_length=250)),
                ('phone', models.CharField(help_text='Phone number/Landline.', max_length=150)),
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
            model_name='certificate',
            name='course_attendee',
            field=models.ForeignKey(to='certification.CourseAttendee'),
        ),
    ]
