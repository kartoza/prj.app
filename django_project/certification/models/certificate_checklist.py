"""Certificate application model for certification apps."""

from django.db import models
from django.utils.translation import ugettext_lazy as _

from certification.models.certifying_organisation import CertifyingOrganisation


class CertificateChecklist(models.Model):
    question = models.CharField(
        help_text=_('Question for certifying organisation applicant.'),
        max_length=1000,
        unique=True,
    )
    sort_number = models.SmallIntegerField(
        help_text=_(
            'The order in which this category is listed within a '
            'project'),
        blank=True,
        null=True
    )
    is_archived = models.BooleanField(
        help_text=_('Is this question archived?'),
        default=False
    )
    is_additional_response_enabled = models.BooleanField(
        help_text=_('Let the applicant add a response when making their '
                    'application.'),
        default=False
    )
    project = models.ForeignKey('base.Project', on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            ('question', 'sort_number'),
        )

    def __str__(self):
        return f'[{self.project.name}] {self.question}'


class CertifyingOrganisationChecklist(models.Model):
    question = models.ForeignKey(
        CertificateChecklist,
        on_delete=models.PROTECT
    )
    certifying_organisation = models.ForeignKey(
        CertifyingOrganisation,
        on_delete=models.CASCADE
    )
    is_checked = models.BooleanField(
        help_text=_('Is the answer is yes or no'),
        null=True
    )
    applicant_response = models.CharField(
        help_text=_('Response from applicant.'),
        max_length=1000,
        blank=True,
        null=True
    )

    class Meta:
        unique_together = (
            ('question', 'certifying_organisation'),
        )

    def __str__(self):
        return f'{self.is_checked}'
