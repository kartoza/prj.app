# coding=utf-8
"""Course model definitions for certification apps.

"""

import datetime
import os
from django.conf.global_settings import MEDIA_ROOT
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
import logging
from unidecode import unidecode
from core.settings.contrib import STOP_WORDS
from .course_convener import CourseConvener
from .certifying_organisation import CertifyingOrganisation
from .course_type import CourseType
from certification.utilities import check_slug
from .training_center import TrainingCenter
from certification.models.certificate_type import CertificateType

logger = logging.getLogger(__name__)


class Course(models.Model):
    """Course model."""

    name = models.CharField(
        help_text=_('Course name.'),
        max_length=200,
        null=True,
        blank=True,
    )

    language = models.CharField(
        help_text=_(
            'A language that the Course will be conducted in, e.g. English.'),
        max_length=200,
        default=_('English'),
        null=True,
        blank=True,
    )

    trained_competence = models.CharField(
        _('Trained competence(s)'),
        help_text=_('Trained competence e.g. Plugin development.'),
        max_length=255,
        null=True,
        blank=True
    )

    start_date = models.DateField(
        _('Start date'),
        help_text=_('Course start date'),
        default=datetime.date.today
    )

    end_date = models.DateField(
        _('End date'),
        help_text=_('Course end date'),
        default=datetime.date.today
    )

    slug = models.CharField(
        max_length=400,
        blank=True,
        default=''
    )

    template_certificate = models.ImageField(
        help_text=_('Background template of the certificate. '
                    'Most browsers support dragging the image directly on to '
                    'the "Choose File" button above.'),
        upload_to=os.path.join(
            MEDIA_ROOT, 'images/organisations/certificates'),
        blank=True
    )

    course_convener = models.ForeignKey(CourseConvener,
                                        on_delete=models.CASCADE)
    course_type = models.ForeignKey(CourseType,
                                    on_delete=models.CASCADE)
    training_center = models.ForeignKey(TrainingCenter,
                                        on_delete=models.CASCADE)
    certifying_organisation = models.ForeignKey(CertifyingOrganisation,
                                                on_delete=models.CASCADE)
    certificate_type = models.ForeignKey(
        CertificateType, on_delete=models.PROTECT, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    objects = models.Manager()

    class Meta:
        ordering = ['name']
        unique_together = [
            'course_convener', 'course_type', 'training_center', 'start_date',
            'end_date', 'certifying_organisation']

    def save(self, *args, **kwargs):
        if not self.pk:
            project_name = self.certifying_organisation.project.name
            course_type_name = self.course_type.name
            self.name = \
                project_name + '_' + course_type_name + '_' + \
                str(self.start_date) + '-' + str(self.end_date)
            registered_course = Course.objects.all()
            words = self.name.split()
            filtered_words = [word for word in words if
                              word.lower() not in STOP_WORDS]
            # unidecode() represents special characters (unicode data) in ASCII
            new_list = unidecode(' '.join(filtered_words))
            new_slug = slugify(new_list)[:100]
            # increment slug when there is duplicate.
            new_slug = check_slug(registered_course, new_slug)
            self.slug = new_slug
        super(Course, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    @property
    def location(self):
        return self.training_center.location

    def get_absolute_url(self):
        """Return URL to course detail page.

        :return: URL
        :rtype: str
        """
        return reverse('course-detail', kwargs={
            'slug': self.slug,
            'organisation_slug': self.certifying_organisation.slug,
            'project_slug': self.certifying_organisation.project.slug
        })

    @property
    def editable(self):
        today = datetime.datetime.today().date()
        delta = self.end_date + datetime.timedelta(days=7)
        if today > delta:
            return False
        else:
            return True
