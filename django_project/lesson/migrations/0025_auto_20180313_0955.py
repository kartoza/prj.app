# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0024_auto_20180312_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specification',
            name='title',
            field=models.CharField(help_text='Title of specification. Markdown is supported', max_length=200),
        ),
        migrations.AlterField(
            model_name='specification',
            name='title_en',
            field=models.CharField(help_text='Title of specification. Markdown is supported', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='specification',
            name='title_ind',
            field=models.CharField(help_text='Title of specification. Markdown is supported', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='specification',
            name='value',
            field=models.CharField(help_text='Value of specification. Markdown is supported', max_length=200),
        ),
        migrations.AlterField(
            model_name='specification',
            name='value_en',
            field=models.CharField(help_text='Value of specification. Markdown is supported', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='specification',
            name='value_ind',
            field=models.CharField(help_text='Value of specification. Markdown is supported', max_length=200, null=True),
        ),
    ]
