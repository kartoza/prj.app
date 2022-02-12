# coding=utf-8
"""Course convener model definitions for certification apps.

"""

import os
from django.conf.global_settings import MEDIA_ROOT
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from core.settings.contrib import STOP_WORDS
from unidecode import unidecode
from certification.models.certifying_organisation import CertifyingOrganisation
from certification.utilities import check_slug


class CourseConvener(models.Model):
    """Course Convener model."""

    slug = models.CharField(
        max_length=100,
        blank=True,
        default=''
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    certifying_organisation = models.ForeignKey(CertifyingOrganisation,
                                                on_delete=models.CASCADE)
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

    is_active = models.BooleanField(
        help_text=_('Inactive Convener will not be available in your '
                    'organisation list.'),
        default=True
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
        new_slug = slugify(new_list)[:50]
        new_slug = check_slug(CourseConvener.objects.all(), new_slug)
        self.slug = slugify(new_slug)[:50]
        super(CourseConvener, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return self.user.username

    @property
    def full_name(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)

    def get_absolute_url(self):
        """Return URL to course convener detail page.

        :return: URL
        :rtype: str
        """
        return reverse('course-convener-detail', kwargs={
            'slug': self.slug,
        })
