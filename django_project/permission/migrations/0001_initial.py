# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0002_project_gitter_room'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectAdministrator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project', models.ForeignKey(to='base.Project')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['project', 'user'],
            },
        ),
        migrations.CreateModel(
            name='ProjectCollaborator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project', models.ForeignKey(to='base.Project')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['project', 'user'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='projectcollaborator',
            unique_together=set([('project', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='projectadministrator',
            unique_together=set([('project', 'user')]),
        ),
    ]
