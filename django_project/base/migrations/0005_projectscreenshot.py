# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_auto_20170908_0715'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectScreenshot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('screenshot', models.ImageField(help_text='A project screenshot.', upload_to=b'images/projects/screenshots', blank=True)),
                ('project', models.ForeignKey(related_name='screenshots', to='base.Project')),
            ],
        ),
    ]
