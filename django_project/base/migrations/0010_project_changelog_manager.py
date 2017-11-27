# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0009_project_certification_manager'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='changelog_manager',
            field=models.ManyToManyField(help_text='Managers of the changelog in this project. They will be allowed to approve changelog entries in the moderation queue.', related_name='changelog_manager', null=True, to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
