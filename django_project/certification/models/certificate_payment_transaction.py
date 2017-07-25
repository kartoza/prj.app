# coding=utf-8

from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from certification.models import Certificate
from certification.models import CertifyingOrganisation


class CertificatePaymentTransaction(models.Model):

    certificate = models.ManyToManyField(Certificate)
    certifying_organisation = models.ForeignKey(CertifyingOrganisation)

    transaction_date = models.DateField(
        _('Transaction Date'),
        help_text=_('Date of the transaction'),
        default=timezone.now
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        ordering = ['transaction_date']

    def __unicode__(self):
        return self.pk

    def save(self, *args, **kwargs):
        super(CertificatePaymentTransaction, self).save(*args, **kwargs)

