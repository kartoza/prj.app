# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certification', '0002_auto_20170316_0539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendee',
            name='certificate',
            field=models.ForeignKey(to='certification.Certificate'),
        ),
        migrations.RemoveField(
            model_name='course',
            name='certificate',
        ),
        migrations.AddField(
            model_name='course',
            name='certificate',
            field=models.ManyToManyField(to='certification.Certificate'),
        ),
    ]
