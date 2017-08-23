# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certification', '0009_auto_20170710_0708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certifyingorganisation',
            name='name',
            field=models.CharField(help_text='name of organisation or institution', max_length=200),
        ),
        migrations.AlterUniqueTogether(
            name='certifyingorganisation',
            unique_together=set([('name', 'project')]),
        ),
    ]
