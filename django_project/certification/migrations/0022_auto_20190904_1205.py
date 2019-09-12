# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certification', '0021_auto_20190904_1205'),
    ]

    operations = [
        migrations.AddField(
            model_name='certifyingorganisation',
            name='status',
            field=models.ForeignKey(to='certification.Status', null=True),
        ),
        migrations.AlterField(
            model_name='certifyingorganisation',
            name='remarks',
            field=models.CharField(help_text='Remarks regarding status of this organisation, i.e. Rejected, because lacks of information', max_length=500, null=True, blank=True),
        ),
    ]
