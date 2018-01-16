# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('changes', '0008_auto_20180108_0848'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsor',
            name='sponsorship_contact_name',
            field=models.CharField(help_text='Full name of sponsorship contact person.', max_length=255, null=True, blank=True),
        ),
    ]
