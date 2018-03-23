# coding=utf-8
"""Course model definitions for certification apps.

"""

import os
from django.conf.global_settings import MEDIA_ROOT
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
import logging
from unidecode import unidecode
from core.settings.contrib import STOP_WORDS
from course_convener import CourseConvener
from certifying_organisation import CertifyingOrganisation
from course_type import CourseType, increment_name
from training_center import TrainingCenter

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
        _('Trained competence'),
        help_text=_('Trained competence e.g. Plugin development.'),
        max_length=255,
        null=True,
        blank=True
    )

    start_date = models.DateField(
        _('Start date'),
        help_text=_('Course start date'),
        default=timezone.now
    )

    end_date = models.DateField(
        _('End date'),
        help_text=_('Course end date'),
        default=timezone.now
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

    course_convener = models.ForeignKey(CourseConvener)
    course_type = models.ForeignKey(CourseType)
    training_center = models.ForeignKey(TrainingCenter)
    certifying_organisation = models.ForeignKey(CertifyingOrganisation)
    author = models.ForeignKey(User)
    objects = models.Manager()

    class Meta:
        ordering = ['name']
        unique_together = [
            'course_convener', 'course_type', 'training_center', 'start_date',
            'end_date', 'certifying_organisation']

    def save(self, *args, **kwargs):
        project_name = self.certifying_organisation.project.name
        course_type_name = self.course_type.name
        self.name = \
            project_name + '_' + course_type_name + '_' + \
            str(self.start_date) + '-' + str(self.end_date)
        registered_course = Course.objects.all()
        name = increment_name(self.name, registered_course)
        words = name.split()
        filtered_words = [word for word in words if
                          word.lower() not in STOP_WORDS]
        # unidecode() represents special characters (unicode data) in ASCII
        new_list = unidecode(' '.join(filtered_words))
        self.slug = slugify(new_list)[:100]
        super(Course, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        """Return URL to course detail page.

        :return: URL
        :rtype: str
        """
        return reverse('course-detail', kwargs={
            'slug': self.slug,
            'certifyingorganisation_slug': self.certifying_organisation.slug
        })
