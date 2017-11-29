# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0010_auto_20171027_0525'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomDomain',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.CharField(default=b'project', max_length=30, choices=[(b'project', b'project'), (b'organisation', b'organisation')])),
                ('custom_domain', models.CharField(help_text='Custom domain, i.e. www.kartoza.com', max_length=30, null=True, blank=True)),
                ('approved', models.BooleanField(default=False, help_text='Whether this user domain has been approved for use yet.')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='customdomain',
            unique_together=set([('user', 'custom_domain')]),
        ),
    ]
