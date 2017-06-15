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
                ('partners', models.TextField(help_text='Funders or Partners of this project.', max_length=3000, blank=True)),
                ('integrations', models.CharField(help_text='Project integrations, e.g. Travis CI.', max_length=1000, blank=True)),
                ('slug', models.SlugField(blank=True)),
                ('project', models.ForeignKey(to='base.Project')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
