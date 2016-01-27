# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Name of this project.', unique=True, max_length=255)),
                ('description', models.CharField(help_text='A description for the project', max_length=500, null=True, blank=True)),
                ('image_file', models.ImageField(help_text='A logo image for this project. Most browsers support dragging the image directly on to the "Choose File" button above.', upload_to=b'images/projects', blank=True)),
                ('approved', models.BooleanField(default=False, help_text='Whether this project has been approved for use yet.')),
                ('private', models.BooleanField(default=False, help_text='Only visible to logged-in users?')),
                ('slug', models.SlugField(unique=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
