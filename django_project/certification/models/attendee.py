# coding=utf-8
"""Attendee model definitions for certification apps.

"""

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from django.contrib.auth.models import User
from core.settings.contrib import STOP_WORDS
from unidecode import unidecode


class Attendee(models.Model):
    """The person who register as attendee is defined here.

    She does not attend any course unless she is defined
    in the Course Attendee model.
    """

    firstname = models.CharField(
        help_text=_('First name of the course attendee.'),
        max_length=200,
        null=False,
        blank=False
    )

    surname = models.CharField(
        help_text=_('Surname of the course attendee.'),
        max_length=200,
        null=False,
        blank=False
    )

    email = models.CharField(
        help_text=_('Email address.'),
        max_length=200,
        null=False,
        blank=False
    )

    slug = models.SlugField()
    author = models.ForeignKey(User)
    objects = models.Manager()

    # noinspection PyClassicStyleClass.
    class Meta:
        ordering = ['firstname']

    def save(self, *args, **kwargs):
        if not self.pk:
            words = self.firstname.split()
            filtered_words = [word for word in
                              words if word.lower() not in STOP_WORDS]
            # unidecode() represents special characters (unicode data) in ASCII
            new_list = unidecode(' '.join(filtered_words))
            self.slug = slugify(new_list)[:50]
        super(Attendee, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s %s' % (self.firstname, self.surname)

    def get_absolute_url(self):
        """Return URL to attendee detail page.

        :return: URL
        :rtype: str
        """
        return reverse('attendee-detail', kwargs={
            'slug': self.slug,
        })
