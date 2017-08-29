# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_project_signature'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='certificate_cost',
            field=models.DecimalField(default=0, null=True, max_digits=10, decimal_places=2, blank=True),
        ),
    ]
