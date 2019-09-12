# coding=utf-8
"""Certificate for certifying organisation
model definitions for certification apps.

"""

from datetime import datetime
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from simple_history.models import HistoricalRecords
from certifying_organisation import CertifyingOrganisation


def increment_id(project):
    """Increment the certificate ID."""

    last_certificate = CertifyingOrganisationCertificate.objects.filter(
        certifying_organisation__project=project
    ).count()

    if last_certificate == 0:
        return '1'

    # get the latest certificate ID within a project
    list_certificates = CertifyingOrganisationCertificate.objects.filter(
        certifying_organisation__project=project
    ).values_list('certificateID', flat=True)
    certificate_array = []
    for certificate in list_certificates:
        number = '{}-'.format(str(project.name).replace(' ', ''))
        certificate_number = str(certificate).replace(number, '')
        certificate_array.append(int(certificate_number))

    new_int_id = max(certificate_array) + 1

    return new_int_id


class CertifyingOrganisationCertificate(models.Model):
    """Certificate for Certifying Organisation model."""

    int_id = models.AutoField(primary_key=True)
    certificateID = models.CharField(
        max_length=100,
        blank=True,
        default=''
    )

    issued = models.DateTimeField(
        default=datetime.now()
    )

    valid = models.BooleanField(
        help_text=_('Is this certificate still valid?'),
        default=True
    )

    author = models.ForeignKey(User)
    certifying_organisation = models.ForeignKey(CertifyingOrganisation)
    history = HistoricalRecords()

    class Meta:
        ordering = ['certificateID']

    def __unicode__(self):
        return self.certificateID

    def save(self, *args, **kwargs):
        if self.int_id is None:
            project_name = self.certifying_organisation.project.name
            words = project_name.replace(' ', '')
            increment_certificate = \
                increment_id(self.certifying_organisation.project)
            self.certificateID = '%s-%s' % (words, str(increment_certificate))
        super(CertifyingOrganisationCertificate, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """Return URL to certificate detail page.

        :return: URL
        :rtype: str
        """
        return reverse('organisation-certificate-detail', kwargs={
            'slug': self.certificateID,
        })
