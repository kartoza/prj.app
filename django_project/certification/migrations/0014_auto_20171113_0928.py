# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('certification', '0012_auto_20170922_0649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendee',
            name='author',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]

