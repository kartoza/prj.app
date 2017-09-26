# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certification', '0011_auto_20170908_1106'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='course',
            unique_together=set([('course_convener', 'course_type', 'training_center', 'start_date', 'end_date', 'certifying_organisation')]),
        ),
        migrations.AlterUniqueTogether(
            name='coursetype',
            unique_together=set([('name', 'certifying_organisation')]),
        ),
    ]
