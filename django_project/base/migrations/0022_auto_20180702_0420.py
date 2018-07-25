# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0021_auto_20180702_0420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_representative_signature',
            field=models.ImageField(help_text='This signature will be used on invoices and certificates. Most browsers support dragging the image directly on to the "Choose File" button above.', upload_to=b'images/projects/signatures', blank=True),
        ),
    ]
