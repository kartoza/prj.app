# coding=utf-8
"""Course model definitions for certification apps.

"""

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
from course_type import CourseType
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

    course_convener = models.ForeignKey(CourseConvener)
    course_type = models.ForeignKey(CourseType)
    training_center = models.ForeignKey(TrainingCenter)
    certifying_organisation = models.ForeignKey(CertifyingOrganisation)
    author = models.ForeignKey(User)
    objects = models.Manager()

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        project_name = self.certifying_organisation.project.name
        course_type_name = self.course_type.name
        self.name = \
            project_name + '_' + course_type_name + '_' + \
            str(self.start_date) + '-' + str(self.end_date)
        words = self.name.split()
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
