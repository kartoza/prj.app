# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0007_remove_specification_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='worksheet',
            name='author_link',
            field=models.URLField(help_text='Link to the author webpage.', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='worksheet',
            name='author_name',
            field=models.TextField(help_text='The author of this worksheet.', max_length=200, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='worksheet',
            name='external_data',
            field=models.FileField(help_text='External data used in this worksheet. Usually a ZIP file. Most browsers support dragging the file directly on to the "Choose File" button above.', upload_to=b'images/lesson/worksheet/external_data', blank=True),
        ),
        migrations.AddField(
            model_name='worksheet',
            name='youtube_link',
            field=models.URLField(help_text='Link to a YouTube video.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='answer_number',
            field=models.IntegerField(default=0, help_text='Used to order the answers for a question into the correct sequence.'),
        ),
        migrations.AlterField(
            model_name='worksheetquestion',
            name='question_number',
            field=models.IntegerField(default=0, help_text='Used to order the questions for a lesson into the correct sequence.'),
        ),
    ]
