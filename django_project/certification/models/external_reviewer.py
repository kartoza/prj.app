from django.db import models
from django.utils import timezone
from django.contrib.sessions.models import Session


class ExternalReviewer(models.Model):

    name = models.CharField(
        max_length=512,
        null=True,
        blank=True,
        help_text='External reviewer name'
    )

    session_key = models.CharField(
        null=False,
        blank=False,
        max_length=100
    )

    certifying_organisation = models.ForeignKey(
        'certification.CertifyingOrganisation',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    email = models.EmailField(
        help_text='Email address of the reviewer',
        null=False,
        blank=False
    )

    @property
    def session_expired(self):
        try:
            session = Session.objects.get(
                pk=self.session_key
            )
            return (
                timezone.now() >
                session.expire_date
            )
        except Session.DoesNotExist:
            return True

    def __str__(self):
        return self.email
