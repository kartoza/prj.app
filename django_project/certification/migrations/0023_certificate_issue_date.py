# Generated by Django 3.2.13 on 2022-06-05 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certification', '0022_externalreviewer_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificate',
            name='issue_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
