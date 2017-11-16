# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certification', '0006_auto_20170622_0812'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='template_certificate',
            field=models.ImageField(help_text='Background template of the certificate. Most browsers support dragging the image directly on to the "Choose File" button above.', upload_to=b'images/organisations/certificates', blank=True),
        ),
    ]
