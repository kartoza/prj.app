# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0022_auto_20180702_0420'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='template_certifying_organisation_certificate',
            field=models.ImageField(help_text='Background template of the certificate for certifying organisation. Most browsers support dragging the image directly on to the "Choose File" button above.', upload_to=b'images/projects/organisation_certificates', blank=True),
        ),
    ]
