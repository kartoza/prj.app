# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('model_id', models.IntegerField()),
                ('model_name', models.CharField(max_length=32)),
                ('model_app_label', models.CharField(max_length=32)),
                ('payment_id', models.CharField(max_length=32)),
                ('time_transaction', models.DateTimeField(default=datetime.datetime.now)),
                ('amount', models.FloatField(help_text='This is amount of money user paid.')),
                ('currency', models.CharField(max_length=4)),
                ('description', models.CharField(max_length=126)),
                ('note', models.CharField(max_length=32, null=True, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
