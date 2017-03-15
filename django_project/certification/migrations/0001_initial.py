# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='CertifyingOrganisation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Name of Organisation or Institution', max_length=200)),
                ('organisation_email', models.CharField(help_text=b'Email address Organisation or Institution', max_length=200)),
                ('organisation_phone', models.CharField(help_text=b'Contact of Organisation or Institution', max_length=200)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='CourseAttendee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'First name course attendee', max_length=200)),
                ('surename', models.CharField(help_text=b'Surename course attendee', max_length=200)),
                ('email', models.CharField(help_text=b'Email address', max_length=200)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='CourseConvener',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'First name of course conveners', max_length=150)),
                ('surename', models.CharField(help_text=b'Surename course conveners', max_length=150)),
                ('email', models.CharField(help_text=b'Email address', max_length=200)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='CourseType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Course type', max_length=200)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('coursetype', models.ForeignKey(to='certification.CourseType')),
            ],
        ),
        migrations.CreateModel(
            name='TrainingCenter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Organisation/Institution name who intend to be a Training Center', unique=True, max_length=150)),
                ('email', models.CharField(help_text='Valid email address for communication purpose', max_length=150)),
                ('Address', models.CharField(help_text='Address of the organisation/institution', max_length=250)),
                ('phone', models.CharField(help_text='Phone number/Landline', max_length=150)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='membership',
            name='trainingcenter',
            field=models.ForeignKey(to='certification.TrainingCenter'),
        ),
        migrations.AddField(
            model_name='coursetype',
            name='training_center',
            field=models.ManyToManyField(to='certification.TrainingCenter', through='certification.Membership'),
        ),
        migrations.AddField(
            model_name='certificate',
            name='student',
            field=models.ForeignKey(to='certification.CourseAttendee'),
        ),
    ]
