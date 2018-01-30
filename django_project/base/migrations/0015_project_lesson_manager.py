# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0014_project_accent_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='lesson_manager',
            field=models.ManyToManyField(help_text='Managers of the lesson app in this project. They will be allowed to create or remove lessons.', related_name='lesson_manager', null=True, to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
