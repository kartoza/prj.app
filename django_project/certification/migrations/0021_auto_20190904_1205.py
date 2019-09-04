# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0022_auto_20180702_0420'),
        ('certification', '0020_auto_20190729_1634'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Name of the status', max_length=200)),
                ('order', models.IntegerField(unique=True, null=True, blank=True)),
                ('project', models.ForeignKey(to='base.Project')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.RenameField(
            model_name='certifyingorganisation',
            old_name='status',
            new_name='remarks',
        ),
        migrations.AlterUniqueTogether(
            name='status',
            unique_together=set([('name', 'project')]),
        ),
    ]
