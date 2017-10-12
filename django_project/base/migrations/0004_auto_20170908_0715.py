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
            name='certificate_credit',
            field=models.IntegerField(default=1, help_text='Cost to issue a certificate, i.e. a certificate cost 1 credit', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='project',
            name='credit_cost',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, blank=True, help_text='Cost for each credit that organisation can buy.', null=True),
        ),
    ]
