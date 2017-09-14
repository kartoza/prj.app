# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_project_gitter_room'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectWebsite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250, null=True, blank=True)),
                ('image', models.ImageField(help_text='A screenshot/diagram for this project. Most browsers support dragging the image directly on to the "Choose File" button above.', upload_to=b'images/project_web', blank=True)),
                ('precis', models.TextField(help_text='Abstract/summary of the project.', max_length=3000, blank=True)),
                ('partners', models.BooleanField(default=False, help_text='Funders or Partners of this project.')),
                ('integrations', models.BooleanField(default=False, help_text='Project integrations, e.g. Travis CI.')),
                ('sponsor', models.BooleanField(default=False, help_text='Sponsor of the project.')),
                ('donations', models.BooleanField(default=False, help_text='Donations for this project.')),
                ('bug_bounties', models.BooleanField(default=False, help_text='Bug bounties for this project.')),
                ('crowd_funding', models.BooleanField(default=False, help_text='Crowd funding for this project.')),
                ('certification', models.BooleanField(default=False, help_text='Certification app of this project.')),
                ('service_providers', models.BooleanField(default=False, help_text='Service providers of this project.')),
                ('store', models.BooleanField(default=False, help_text='Store that sells items/merchandise of this project.')),
                ('changelog', models.BooleanField(default=True, help_text='Changelog app of this project (releases).')),
                ('developer_map', models.BooleanField(default=True, help_text='Developers who build this project.')),
                ('user_map', models.BooleanField(default=True, help_text='Users')),
                ('upcoming_events', models.BooleanField(default=True, help_text='News and upcoming events.')),
                ('project_teams', models.BooleanField(default=True, help_text='Project Teams')),
                ('votes', models.BooleanField(default=True, help_text='Votes')),
                ('slug', models.SlugField(blank=True)),
                ('project', models.ForeignKey(to='base.Project')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
