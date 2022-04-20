from django.contrib.auth.models import User
from django.db import models

from certification.models import CHECKLIST_CHOICES


class OrganisationChecklist(models.Model):

    checklist = models.ForeignKey(
        'certification.Checklist',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    checklist_target = models.CharField(
        choices=CHECKLIST_CHOICES,
        max_length=100,
        blank=True,
        default=''
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True
    )

    organisation = models.ForeignKey(
        'certification.CertifyingOrganisation',
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )

    checklist_question = models.TextField(
        blank=False,
        null=False,
        help_text='Original question from checklist.'
    )

    checked = models.BooleanField(
        default=False,
        help_text='Indicate whether the checklist is checked or not.'
    )

    text_box_content = models.TextField(
        blank=True,
        null=True,
        help_text='Content in text box if available.'
    )

    submitter = models.ForeignKey(
        User,
        related_name='checklist_submitter',
        blank=True,
        null=True,
        help_text='User who submitted the checklist.',
        on_delete=models.SET_NULL
    )

    external_submitter = models.ForeignKey(
        'certification.ExternalReviewer',
        related_name='checklist_external_submitter',
        blank=True,
        null=True,
        help_text='External reviewer who submitted'
                  ' the checklist.',
        on_delete=models.SET_NULL
    )
