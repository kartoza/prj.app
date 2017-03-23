# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
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
                ('organisation_phone', models.CharField(help_text=b'Contact of Organisation or Institution.', max_length=200)),
                ('approved', models.BooleanField(default=False, help_text=b'Approval from project admin')),
                ('slug', models.SlugField()),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Course name.', max_length=200)),
                ('slug', models.SlugField()),
                ('certificate', models.ManyToManyField(to='certification.Certificate')),
                ('course_attendee', models.ManyToManyField(to='certification.Attendee')),
            ],
        ),
        migrations.CreateModel(
            name='CourseConvener',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Course convener name', max_length=250)),
                ('email', models.CharField(help_text=b'Course convener email', max_length=150, null=True, blank=True)),
                ('slug', models.SlugField()),
                ('course', models.ManyToManyField(to='certification.Course')),
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
                ('slug', models.SlugField(unique=True)),
                ('course', models.ManyToManyField(to='certification.Course')),
            ],
            options={
                'ordering': ['name'],
            },
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
                ('course', models.ManyToManyField(to='certification.Course')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='certifyingorganisation',
            name='course',
            field=models.ManyToManyField(to='certification.Course'),
        ),
        migrations.AddField(
            model_name='certifyingorganisation',
            name='course_convener',
            field=models.ManyToManyField(to='certification.CourseConvener'),
        ),
        migrations.AddField(
            model_name='certifyingorganisation',
            name='course_type',
            field=models.ManyToManyField(to='certification.CourseType'),
        ),
        migrations.AddField(
            model_name='certifyingorganisation',
            name='training_center',
            field=models.ManyToManyField(to='certification.TrainingCenter'),
        ),
        migrations.AddField(
            model_name='attendee',
            name='certificate',
            field=models.ForeignKey(to='certification.Certificate'),
        ),
    ]
