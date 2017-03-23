# coding=utf-8
"""
Training center model definitions for certification apps
"""

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from core.settings.contrib import STOP_WORDS
from unidecode import unidecode
from course import Course


class TrainingCenter(models.Model):
    """Training Centre / Organisation registration."""

    name = models.CharField(
        help_text=_('Organisation/Institution name.'),
        max_length=150,
        null=False,
        blank=False,
        unique=True
    )

    email = models.CharField(
        help_text=_('Valid email address for communication purpose.'),
        max_length=150,
        null=False,
        blank=False
    )

    address = models.TextField(
        help_text=_('Address of the organisation/institution.'),
        max_length=250,
        null=False,
        blank=False,
    )

    phone = models.CharField(
        help_text=_('Phone number/Landline.'),
        max_length=150,
        null=False,
        blank=False
    )

    slug = models.SlugField()
    objects = models.Manager()
    course = models.ManyToManyField(Course)

    # noinspection PyClassicStyleClass.
    class Meta:
        """Meta class for training centre."""

        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.pk:
            words = self.name.split()
            filtered_words = [t for t in words if t.lower() not in STOP_WORDS]
            # unidecode() represents special characters (unicode data) in ASCII
            new_list = unidecode(' '.join(filtered_words))
            self.slug = slugify(new_list)[:50]

        super(TrainingCenter, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s' % self.name

    def get_absolute_url(self):
        """Return URL to training center detail page.
        :return: URL
        :rtype: str
        """
        return reverse('training-center-detail', kwargs={'slug': self.slug})
