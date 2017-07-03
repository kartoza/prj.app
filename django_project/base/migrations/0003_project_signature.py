# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_project_gitter_room'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='signature',
            field=models.ImageField(help_text='Signature of the project owner. Most browsers support dragging the image directly on to the "Choose File" button above.', upload_to=b'images/projects/signatures', blank=True),
        ),
    ]
