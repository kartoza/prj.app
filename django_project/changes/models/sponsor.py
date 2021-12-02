# coding=utf-8
import os
import pytz
import logging
from django.urls import reverse
from django.utils.text import slugify
from core.settings.contrib import STOP_WORDS
from django.conf.global_settings import MEDIA_ROOT
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from unidecode import unidecode


__author__ = 'rischan'

logger = logging.getLogger(__name__)
utc = pytz.UTC


def active_sustaining_membership(user, project):
    """Returns active sustaining membership from user and project."""
    if user.is_anonymous:
        return Sponsor.objects.none()
    sustaining_members = Sponsor.objects.filter(
        author=user,
        project=project,
        sustaining_membership=True,
        active=True
    )
    return sustaining_members


def validate_email_address(value):
    try:
        validate_email(value)
        return True
    except ValidationError:
        raise ValidationError(
            _('%(value)s is not a valid email address'),
            params={'value': value},
        )


class ApprovedSponsorManager(models.Manager):
    """Custom sponsor manager that shows only approved records."""

    def get_queryset(self):
        """Query set generator."""
        return super(
            ApprovedSponsorManager, self).get_queryset().filter(
                approved=True)


class UnapprovedSponsorManager(models.Manager):
    """Custom sponsor manager that shows only unapproved records."""

    def get_queryset(self):
        """Query set generator."""
        return super(
            UnapprovedSponsorManager, self).get_queryset().filter(
                approved=False)


class PendingSponsorManager(models.Manager):
    """Custom manager that shows unapproved and unrejected records."""
    def get_queryset(self):
        return super(
            PendingSponsorManager, self
        ).get_queryset().filter(
            approved=False,
            rejected=False
        )


# noinspection PyUnresolvedReferences
class Sponsor(models.Model):
    """A sponsor model e.g. gui, backend, web site etc."""
    name = models.CharField(
        help_text=_('Name of organisation or individual.'),
        max_length=255,
        null=False,
        blank=False,
        unique=False)  # there is a unique together rule in meta class below

    contact_title = models.CharField(
        _('Representative Title'),
        max_length=255,
        null=True,
        blank=True,
        help_text=_('Title of the representative i.e Treasurer.')
    )

    sponsor_url = models.CharField(
        _('Organisation URL'),
        help_text=_('Website for the organisation or individual.'),
        max_length=255,
        null=True,
        blank=True,
    )

    contact_person = models.CharField(
        help_text=_('Input the contact person.'),
        max_length=255,
        null=True,
        blank=True)

    address = models.TextField(
        help_text=(
            'Provide your / your organisation\'s complete address. '
            'Use line breaks...'
        ),
        null=True,
        blank=True)

    country = CountryField(
        help_text=_('Select the country.'),
        null=True,
        blank=True)

    sponsor_email = models.CharField(
        _('Contact Email'),
        help_text=_('Enter the email of the contact person.'),
        max_length=255,
        null=True,
        blank=True,
        validators=[validate_email_address],
    )

    agreement = models.FileField(
        help_text='Attach sponsor agreement',
        upload_to=os.path.join(MEDIA_ROOT, 'docs'),
        blank=True)

    logo = models.ImageField(
        help_text=_(
            'An image of your / your organisation logo e.g. a splashscreen. '
            'Most browsers support dragging the image directly on to the '
            '"Choose File" button above.'),
        upload_to=os.path.join(MEDIA_ROOT, 'images/projects'),
        blank=False)

    approved = models.BooleanField(
        help_text=_(
            'Whether this sponsor has been approved for use by the '
            'project owner.'),
        default=False
    )

    rejected = models.BooleanField(
        help_text=_(
            'Whether this sustaining member has been rejected for use by the '
            'project manager.'),
        default=False
    )

    remarks = models.CharField(
        help_text=_(
            'Remarks regarding status of this sustaining members, '
            'i.e. Rejected, because lacks of information'),
        max_length=500,
        null=True,
        blank=True
    )

    invoice_number = models.CharField(
        _("Sponsorship invoice number"),
        max_length=255,
        null=True,
        blank=True,
        help_text=_("Invoice number for the sponsor.")
    )

    sustaining_membership = models.BooleanField(
        _("Check if this data is sustaining membership"),
        default=False
    )

    active = models.BooleanField(
        _("Check if this sustaining member is active"),
        default=True
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField()
    project = models.ForeignKey('base.Project', on_delete=models.CASCADE)
    objects = models.Manager()
    approved_objects = ApprovedSponsorManager()
    unapproved_objects = UnapprovedSponsorManager()
    pending_objects = PendingSponsorManager()

    # noinspection PyClassicStyleClass
    class Meta:
        """Meta options for the sponsor class."""
        unique_together = (
            ('name', 'project'),
            ('project', 'slug')
        )
        app_label = 'changes'
        ordering = ['project', 'name']
        verbose_name = 'Sustaining Member'
        verbose_name_plural = 'Sustaining Members'

    def save(self, *args, **kwargs):
        if not self.pk:
            words = self.name.split()
            filtered_words = [t for t in words if t.lower() not in STOP_WORDS]
            # unidecode() represents special characters (unicode data) in ASCII
            new_list = unidecode(' '.join(filtered_words))
            self.slug = slugify(new_list)[:50]

        if self.active and active_sustaining_membership(
            self.author,
            self.project
        ).count() > 1:
            raise ValidationError('More than one sustaining member for '
                                  'same user and project is not allowed')

        super(Sponsor, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'{}'.format(self.name)

    def __str__(self):
        return '{}'.format(self.name)

    def get_absolute_url(self):
        return reverse('sponsor-detail', kwargs={
            'slug': self.slug,
            'project_slug': self.project.slug
        })
