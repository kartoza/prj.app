# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('certification', '0013_auto_20171014_1045'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courseconvener',
            name='degree',
        ),
        migrations.RemoveField(
            model_name='courseconvener',
            name='title',
        ),
        migrations.AlterField(
            model_name='attendee',
            name='author',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='certifyingorganisation',
            name='name',
            field=models.CharField(help_text='name of organisation or institution', max_length=200),
        ),
    ]
