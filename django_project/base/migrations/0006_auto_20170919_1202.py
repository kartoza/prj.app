# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_projectscreenshot'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='precis',
            field=models.TextField(help_text='A detailed summary of the project.', max_length=2000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.CharField(help_text='A short description for the project', max_length=500, null=True, blank=True),
        ),
    ]
