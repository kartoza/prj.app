# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certification', '0016_course_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='trained_competence',
            field=models.CharField(help_text='Trained competence e.g. Plugin development.', max_length=255, null=True, verbose_name='Trained competence', blank=True),
        ),
    ]
