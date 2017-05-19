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
from certifying_organisation import validate_email_address


def increment_slug(_firstname, _surname):
    """Function to increment slug.

    If there is already attendee that is registered in the system
    who has the same firstname and surname with the new attendee
    that will be registered, the slug will be incremented
    e.g. anita-hapsari, anita-hapsari-2, anita-hapsari-3, etc.

    """

    registered_attendee = Attendee.objects.all()
    new_name = '%s %s' % (_firstname, _surname)
    for attendee in registered_attendee:
        if _firstname == attendee.firstname and _surname == attendee.surname:
            _name = Attendee.objects.filter(
                firstname=_firstname, surname=_surname)
            count = _name.count() + 1
            new_name = '%s %s %s' % (_firstname, _surname, count)
            break

    return new_name


class Attendee(models.Model):
    """The person who register as attendee is defined here.

    She does not attend any course unless she is defined
    in the Course Attendee model.
    """

    firstname = models.CharField(
        help_text=_('First name of the attendee.'),
        max_length=200,
        null=False,
        blank=False
    )

    surname = models.CharField(
        help_text=_('Surname of the attendee.'),
        max_length=200,
        null=False,
        blank=False
    )

    email = models.CharField(
        help_text=_('Email address.'),
        max_length=200,
        null=False,
        blank=False,
        validators=[validate_email_address]
    )

    slug = models.SlugField()
    author = models.ForeignKey(User)
    objects = models.Manager()

    # noinspection PyClassicStyleClass.
    class Meta:
        ordering = ['firstname']
        unique_together = [
            'firstname', 'surname', 'email'
        ]

    def save(self, *args, **kwargs):
        if not self.pk:
            name = increment_slug(self.firstname, self.surname)
            words = name.split()
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
