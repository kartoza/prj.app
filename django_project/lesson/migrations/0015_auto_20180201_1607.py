# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0014_auto_20180129_1339'),
    ]

    operations = [
        migrations.AddField(
            model_name='worksheet',
            name='exercise_image',
            field=models.ImageField(help_text='Image for the exercise part. You should normally either use the Requirements table or this image field. A landscape image, approximately 800*200. Most browsers support dragging the image directly on to the "Choose File" button above.', upload_to=b'images/lesson/worksheet/exercise', blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='answer',
            unique_together=set([]),
        ),
        migrations.AlterUniqueTogether(
            name='section',
            unique_together=set([]),
        ),
        migrations.AlterUniqueTogether(
            name='specification',
            unique_together=set([]),
        ),
        migrations.AlterUniqueTogether(
            name='worksheet',
            unique_together=set([]),
        ),
        migrations.AlterUniqueTogether(
            name='worksheetquestion',
            unique_together=set([]),
        ),
    ]
