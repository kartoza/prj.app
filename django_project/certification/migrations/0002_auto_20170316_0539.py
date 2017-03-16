# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import certification.models


class Migration(migrations.Migration):

    dependencies = [
        ('certification', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('firstname', models.CharField(help_text=b'First name course attendee.', max_length=200)),
                ('surname', models.CharField(help_text=b'Surname course attendee.', max_length=200)),
                ('email', models.CharField(help_text=b'Email address.', max_length=200)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'ordering': ['firstname'],
            },
            bases=(certification.models.SlugModel, models.Model),
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Course name.', max_length=200)),
                ('slug', models.SlugField(unique=True)),
            ],
            bases=(certification.models.SlugModel, models.Model),
        ),
        migrations.RemoveField(
            model_name='membership',
            name='coursetype',
        ),
        migrations.RemoveField(
            model_name='membership',
            name='trainingcenter',
        ),
        migrations.AlterModelOptions(
            name='courseconvener',
            options={},
        ),
        migrations.RemoveField(
            model_name='certificate',
            name='student',
        ),
        migrations.RemoveField(
            model_name='courseconvener',
            name='email',
        ),
        migrations.RemoveField(
            model_name='courseconvener',
            name='name',
        ),
        migrations.RemoveField(
            model_name='courseconvener',
            name='surename',
        ),
        migrations.RemoveField(
            model_name='coursetype',
            name='training_center',
        ),
        migrations.AddField(
            model_name='certifyingorganisation',
            name='approved',
            field=models.BooleanField(default=False, help_text=b'Approval from project admin'),
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
        migrations.AlterField(
            model_name='certifyingorganisation',
            name='name',
            field=models.CharField(help_text=b'Name of Organisation or Institution.', max_length=200),
        ),
        migrations.AlterField(
            model_name='certifyingorganisation',
            name='organisation_email',
            field=models.CharField(help_text=b'Email address Organisation or Institution.', max_length=200),
        ),
        migrations.AlterField(
            model_name='certifyingorganisation',
            name='organisation_phone',
            field=models.CharField(help_text=b'Contact of Organisation or Institution.', max_length=200),
        ),
        migrations.AlterField(
            model_name='coursetype',
            name='name',
            field=models.CharField(help_text=b'Course type.', max_length=200),
        ),
        migrations.AlterField(
            model_name='trainingcenter',
            name='Address',
            field=models.CharField(help_text='Address of the organisation/institution.', max_length=250),
        ),
        migrations.AlterField(
            model_name='trainingcenter',
            name='email',
            field=models.CharField(help_text='Valid email address for communication purpose.', max_length=150),
        ),
        migrations.AlterField(
            model_name='trainingcenter',
            name='name',
            field=models.CharField(help_text='Organisation/Institution name.', unique=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='trainingcenter',
            name='phone',
            field=models.CharField(help_text='Phone number/Landline.', max_length=150),
        ),
        migrations.DeleteModel(
            name='CourseAttendee',
        ),
        migrations.DeleteModel(
            name='Membership',
        ),
        migrations.AddField(
            model_name='course',
            name='certificate',
            field=models.ForeignKey(to='certification.Certificate', to_field=django.db.models.deletion.CASCADE),
        ),
        migrations.AddField(
            model_name='course',
            name='course_attendee',
            field=models.ManyToManyField(to='certification.Attendee'),
        ),
        migrations.AddField(
            model_name='attendee',
            name='certificate',
            field=models.ForeignKey(to='certification.Certificate', to_field=django.db.models.deletion.CASCADE),
        ),
        migrations.AddField(
            model_name='certifyingorganisation',
            name='course',
            field=models.ManyToManyField(to='certification.Course'),
        ),
        migrations.AddField(
            model_name='courseconvener',
            name='course',
            field=models.ManyToManyField(to='certification.Course'),
        ),
        migrations.AddField(
            model_name='coursetype',
            name='course',
            field=models.ManyToManyField(to='certification.Course'),
        ),
        migrations.AddField(
            model_name='trainingcenter',
            name='course',
            field=models.ManyToManyField(to='certification.Course'),
        ),
    ]
