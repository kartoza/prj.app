# Generated by Django 2.2.18 on 2022-03-23 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certification', '0011_auto_20220321_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checklist',
            name='order',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='historicalchecklist',
            name='order',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
