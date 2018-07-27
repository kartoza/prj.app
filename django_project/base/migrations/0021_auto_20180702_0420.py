# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0020_auto_20180226_1401'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='signature',
            new_name='project_representative_signature',
        ),
        migrations.AddField(
            model_name='project',
            name='project_representative',
            field=models.ForeignKey(related_name='project_representative', blank=True, to=settings.AUTH_USER_MODEL, help_text='Project representative. This name will be used on invoices and certificates. ', null=True),
        ),
    ]
