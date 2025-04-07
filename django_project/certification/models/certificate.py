# coding=utf-8
"""Certificate model definitions for certification apps.

"""

from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from .course import Course
from .attendee import Attendee
from .certificate_type import CertificateType


def increment_id(project):
    """Increment the certificate ID."""

    last_certificate = Certificate.objects.filter(
        course__certifying_organisation__project=project
    ).count()

    if last_certificate == 0:
        return '1'

    # get the latest certificate ID within a project
    list_certificates = Certificate.objects.filter(
        course__certifying_organisation__project=project
    ).values_list('certificateID', flat=True)
    certificate_array = []
    for certificate in list_certificates:
        number = '{}-'.format(str(project.name).replace(' ', ''))
        certificate_number = str(certificate).replace(number, '')
        certificate_array.append(int(certificate_number))

    new_int_id = max(certificate_array) + 1

    return new_int_id


class Certificate(models.Model):
    """Certificate model."""

    int_id = models.AutoField(primary_key=True)
    certificateID = models.CharField(
        max_length=100,
        blank=True,
        default=''
    )

    is_paid = models.BooleanField(
        help_text=_('Is this certificate paid?'),
        default=False
    )

    issue_date = models.DateField(
        auto_now_add=True,
        blank=True,
        null=True
    )

    certificate_type = models.ForeignKey(
        CertificateType, on_delete=models.PROTECT, null=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    objects = models.Manager()

    class Meta:
        ordering = ['certificateID']
        unique_together = [
            'course', 'attendee',
        ]

    def __unicode__(self):
        return self.certificateID

    def save(self, *args, **kwargs):
        if self.int_id is None:
            project_name = self.course.certifying_organisation.project.name
            words = project_name.replace(' ', '')
            increment_certificate = \
                increment_id(self.course.certifying_organisation.project)
            self.certificateID = '%s-%s' % (words, str(increment_certificate))
        super(Certificate, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """Return URL to certificate detail page.

        :return: URL
        :rtype: str
        """
        return reverse('certificate-detail', kwargs={
            'slug': self.certificateID,
        })
