# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import base.models.project


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='gitter_room',
            field=models.CharField(blank=True, max_length=255, null=True, help_text='Gitter room name, e.g. gitterhq/sandbox', validators=[base.models.project.validate_gitter_room_name]),
        ),
    ]
