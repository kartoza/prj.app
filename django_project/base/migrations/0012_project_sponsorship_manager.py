# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0011_project_changelog_manager'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='sponsorship_manager',
            field=models.ManyToManyField(help_text='Managers of the sponsorship in this project. They will be allowed to approve sponsor entries in the moderation queue.', related_name='sponsorship_manager', null=True, to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
