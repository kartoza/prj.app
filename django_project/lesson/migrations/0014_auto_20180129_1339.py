# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0013_auto_20180127_0626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worksheet',
            name='more_about_text',
            field=models.TextField(help_text='More detail about the content of the worksheet. Markdown is supported.'),
        ),
        migrations.AlterField(
            model_name='worksheet',
            name='more_about_text_en',
            field=models.TextField(help_text='More detail about the content of the worksheet. Markdown is supported.', null=True),
        ),
        migrations.AlterField(
            model_name='worksheet',
            name='more_about_text_ind',
            field=models.TextField(help_text='More detail about the content of the worksheet. Markdown is supported.', null=True),
        ),
        migrations.AlterField(
            model_name='worksheet',
            name='summary_text',
            field=models.TextField(help_text='Content of the summary. Markdown is supported.'),
        ),
        migrations.AlterField(
            model_name='worksheet',
            name='summary_text_en',
            field=models.TextField(help_text='Content of the summary. Markdown is supported.', null=True),
        ),
        migrations.AlterField(
            model_name='worksheet',
            name='summary_text_ind',
            field=models.TextField(help_text='Content of the summary. Markdown is supported.', null=True),
        ),
    ]
