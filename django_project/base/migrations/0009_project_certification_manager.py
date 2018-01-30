# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0008_project_sponsorship_programme'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='certification_manager',
            field=models.ManyToManyField(help_text='Managers of the certification app in this project. They will receive email notification about organisation and have the same permissions as project owner in the certification app.', related_name='certification_manager', null=True, to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
