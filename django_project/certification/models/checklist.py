from django.db import models
from django.utils.translation import ugettext_lazy as _
from simple_history.models import HistoricalRecords

ORGANIZATION_OWNER = 'organization_owner'
REVIEWER = 'reviewer'

CHECKLIST_CHOICES = (
    (ORGANIZATION_OWNER, 'Organization Owner'),
    (REVIEWER, 'Reviewer'),
)


class Checklist(models.Model):

    project = models.ForeignKey(
        'base.Project',
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )

    order = models.IntegerField(
        blank=True,
        null=True
    )

    question = models.TextField(
        blank=False,
        null=False,
        help_text='Checklist question for certification application form, e.g.'
                  ' Have you contributed to documentation?'
    )

    help_text = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )

    active = models.BooleanField(
        default=False
    )

    show_text_box = models.BooleanField(
        help_text=_('Indicate whether the user should see a '
                    'text box to add detail or not'),
        default=False
    )

    approved = models.BooleanField(
        help_text=_('Approval from project admin'),
        default=False
    )

    remarks = models.CharField(
        help_text=_(
            'Remarks regarding status of this checklist, '
            'i.e. Rejected, because lacks of information'),
        max_length=500,
        null=True,
        blank=True
    )

    target = models.CharField(
        choices=CHECKLIST_CHOICES,
        max_length=100,
        blank=True,
        default=''
    )

    history = HistoricalRecords()

    @property
    def creator(self):
        try:
            return self.history.earliest().history_user
        except: # noqa, history does not exist
            return None

    def __str__(self):
        return self.question
