# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ballot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Name of this ballot.', max_length=255)),
                ('summary', models.CharField(help_text='A brief overview of the ballot.', max_length=250)),
                ('description', models.TextField(help_text='A full description of the proposal if a summary is not enough!', max_length=3000, null=True, blank=True)),
                ('approved', models.BooleanField(default=False, help_text='Whether this ballot has been approved.')),
                ('denied', models.BooleanField(default=False, help_text='Whether this ballot has been denied.')),
                ('no_quorum', models.BooleanField(default=False, help_text='Whether the ballot was denied because no quorum was reached')),
                ('open_from', models.DateTimeField(default=django.utils.timezone.now, help_text='Date the ballot opens')),
                ('closes', models.DateTimeField(default=datetime.datetime(2015, 11, 20, 15, 9, 38, 554659, tzinfo=utc), help_text='Date the ballot closes')),
                ('private', models.BooleanField(default=False, help_text='Should members be prevented from viewing results before voting?')),
                ('slug', models.SlugField()),
            ],
        ),
        migrations.CreateModel(
            name='Committee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='The name of this committee.', max_length=255)),
                ('description', models.TextField(help_text="A description of the committee's role within the project.", max_length=1000, null=True, blank=True)),
                ('sort_number', models.SmallIntegerField(default=0, help_text='The order in which this committee is listed within a project')),
                ('quorum_setting', models.CharField(help_text='The percentage of committee members required to vote in order to have quorum', max_length=3, choices=[(b'100', b'All Members'), (b'75', b'Three Quarters'), (b'50', b'Half'), (b'25', b'One Quarter'), (b'1', b'One Member')])),
                ('slug', models.SlugField()),
                ('chair', models.ForeignKey(related_name='committee_chairman', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(to='base.Project')),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('choice', models.CharField(default=b'-', max_length=1, choices=[(b'y', b'Yes'), (b'-', b'Abstain'), (b'n', b'No')])),
                ('ballot', models.ForeignKey(to='vota.Ballot')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='ballot',
            name='committee',
            field=models.ForeignKey(to='vota.Committee'),
        ),
        migrations.AddField(
            model_name='ballot',
            name='proposer',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set([('user', 'ballot')]),
        ),
        migrations.AlterUniqueTogether(
            name='committee',
            unique_together=set([('project', 'slug'), ('name', 'project')]),
        ),
        migrations.AlterUniqueTogether(
            name='ballot',
            unique_together=set([('name', 'committee'), ('committee', 'slug')]),
        ),
    ]
