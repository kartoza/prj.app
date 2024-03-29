# Generated by Django 2.2.18 on 2021-12-10 08:31

from django.db import migrations, models
import django.db.models.deletion

def set_existing_certificate_type_value(apps, shcema_editor):
    CertificateType = apps.get_model('certification', 'CertificateType')
    Course = apps.get_model('certification', 'Course')
    certificate_type = CertificateType.objects.filter(
        name='attendance and completion').first()
    courses = Course.objects.all()

    for course in courses:
        course.certificate_type = certificate_type
        course.save(update_fields=['certificate_type'])


class Migration(migrations.Migration):

    dependencies = [
        ('certification', '0008_projectcertificatetype'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='certificate_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='certification.CertificateType'),
        ),

        migrations.RunPython(set_existing_certificate_type_value, reverse_code=migrations.RunPython.noop),

        migrations.AlterField(
            model_name='course',
            name='certificate_type',
            field=models.ForeignKey(null=False, on_delete=django.db.models.deletion.PROTECT,
                                    to='certification.CertificateType'),
            preserve_default=False,
        ),

    ]
