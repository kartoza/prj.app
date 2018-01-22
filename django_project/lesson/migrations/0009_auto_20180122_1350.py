# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0008_auto_20180122_1033'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'ordering': ['question', 'answer_number']},
        ),
        migrations.AlterModelOptions(
            name='furtherreading',
            options={'ordering': ['worksheet']},
        ),
        migrations.AlterModelOptions(
            name='section',
            options={'ordering': ['project', 'section_number']},
        ),
        migrations.AlterModelOptions(
            name='specification',
            options={'ordering': ['worksheet', 'specification_number']},
        ),
        migrations.AlterModelOptions(
            name='worksheet',
            options={'ordering': ['section', 'order_number']},
        ),
        migrations.AlterModelOptions(
            name='worksheetquestion',
            options={'ordering': ['question', 'question_number']},
        ),
        migrations.AddField(
            model_name='worksheet',
            name='order_number',
            field=models.IntegerField(default=0, help_text='The order in which this worksheet is listed within a section', verbose_name='Worksheet number'),
        ),
        migrations.AlterUniqueTogether(
            name='answer',
            unique_together=set([('question', 'answer_number')]),
        ),
        migrations.AlterUniqueTogether(
            name='section',
            unique_together=set([('project', 'section_number')]),
        ),
        migrations.AlterUniqueTogether(
            name='specification',
            unique_together=set([('worksheet', 'specification_number')]),
        ),
        migrations.AlterUniqueTogether(
            name='worksheet',
            unique_together=set([('section', 'order_number')]),
        ),
    ]
