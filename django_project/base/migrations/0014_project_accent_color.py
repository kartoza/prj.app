# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import colorfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_auto_20180103_0937'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='accent_color',
            field=colorfield.fields.ColorField(default=b'#FF0000', max_length=18, null=True, help_text='A color represent the project color', blank=True),
        ),
    ]
