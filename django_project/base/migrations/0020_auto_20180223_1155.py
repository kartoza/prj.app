# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0019_project_project_repository_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='image_file',
            field=models.ImageField(help_text='A logo image for this project. Most browsers support dragging the image directly on to the "Choose File" button above. The ideal size for your image is 512 x 512 pixels.', upload_to=b'images/projects', blank=True),
        ),
    ]
