# coding=utf-8
"""Course convener model definitions for certification apps.

"""

import os
from django.conf.global_settings import MEDIA_ROOT
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from core.settings.contrib import STOP_WORDS
from unidecode import unidecode
from certifying_organisation import CertifyingOrganisation


class CourseConvener(models.Model):
    """Course Convener model."""

    slug = models.CharField(
        max_length=100,
        blank=True,
        default=''
    )

    user = models.ForeignKey(User)
    certifying_organisation = models.ForeignKey(CertifyingOrganisation)
    objects = models.Manager()

    signature = models.ImageField(
        help_text=_('Signature of the course convener. '
                    'Most browsers support dragging the image directly on to '
                    'the "Choose File" button above.'),
        upload_to=os.path.join(MEDIA_ROOT, 'images/organisations/conveners'),
        blank=True
    )

    title = models.CharField(
        help_text=_('Title of the course convener, e.g. Prof.'),
        max_length=50,
        blank=True,
        null=True
    )

    degree = models.CharField(
        help_text=_('Degree of the course convener, e.g. MSc.'),
        max_length=50,
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['user']

    def save(self, *args, **kwargs):
        words = self.certifying_organisation.name.split()
        filtered_words = [word for word in words if
                          word.lower() not in STOP_WORDS]
        # unidecode() represents special characters (unicode data) in ASCII
        new_list = '%s-%s' % \
                   (self.user.username, unidecode(' '.join(filtered_words)))
        self.slug = slugify(new_list)[:50]
        super(CourseConvener, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.user.username

    def get_absolute_url(self):
        """Return URL to course convener detail page.

        :return: URL
        :rtype: str
        """
        return reverse('course-convener-detail', kwargs={
            'slug': self.slug,
        })
