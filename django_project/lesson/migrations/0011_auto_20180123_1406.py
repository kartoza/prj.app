# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lesson', '0010_auto_20180123_0959'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'ordering': ['question', 'sequence_number']},
        ),
        migrations.AlterModelOptions(
            name='section',
            options={'ordering': ['project', 'sequence_number']},
        ),
        migrations.AlterModelOptions(
            name='specification',
            options={'ordering': ['worksheet', 'sequence_number']},
        ),
        migrations.AlterModelOptions(
            name='worksheet',
            options={'ordering': ['section', 'sequence_number']},
        ),
        migrations.AlterModelOptions(
            name='worksheetquestion',
            options={'ordering': ['question', 'sequence_number']},
        ),
        migrations.RenameField(
            model_name='answer',
            old_name='answer_number',
            new_name='sequence_number',
        ),
        migrations.RenameField(
            model_name='section',
            old_name='section_number',
            new_name='sequence_number',
        ),
        migrations.RenameField(
            model_name='specification',
            old_name='specification_number',
            new_name='sequence_number',
        ),
        migrations.RenameField(
            model_name='worksheet',
            old_name='order_number',
            new_name='sequence_number',
        ),
        migrations.RenameField(
            model_name='worksheetquestion',
            old_name='question_number',
            new_name='sequence_number',
        ),
        migrations.AlterUniqueTogether(
            name='answer',
            unique_together=set([('question', 'sequence_number')]),
        ),
        migrations.AlterUniqueTogether(
            name='section',
            unique_together=set([('project', 'sequence_number')]),
        ),
        migrations.AlterUniqueTogether(
            name='specification',
            unique_together=set([('worksheet', 'sequence_number')]),
        ),
        migrations.AlterUniqueTogether(
            name='worksheet',
            unique_together=set([('section', 'sequence_number')]),
        ),
        migrations.AlterUniqueTogether(
            name='worksheetquestion',
            unique_together=set([('sequence_number', 'question')]),
        ),
    ]
