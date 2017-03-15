
import os
import logging
import string
import re
from django.core.urlresolvers import reverse
# from __future__ import unicode_literals
from django.db import models
from django.utils.text import slugify
from django.conf.global_settings import MEDIA_ROOT
from django.utils.translation import ugettext_lazy as _
from core.settings.contrib import STOP_WORDS
from django.conf import settings
from django.core.exceptions import ValidationError
from unidecode import unidecode


logger = logging.getLogger(__name__)

class ApprovedTrainingCenterManager(models.Manager):
    """ Custom training centre manager that shows only approved conveners """

    def get_queryset(self):
        """ Query set generator """
        return super(
            ApprovedTrainingCenterManager, self).get_queryset().filter(approved=True)


class UnapprovedTrainingCenterManager(models.Manager):
    """ Custom training centre manager that shows only unapproved training centre """

    def get_queryset(self):
        """ Query set generator """
        return super(
            UnapprovedTrainingCenterManager, self).get_queryset().filter(approved=False)


class TrainingCenter(models.Model):
    """ Training Centre / Organisation registration """
    name = models.CharField(
        help_text=_('Organisation/Institution name who intend to be a Training Center'),
        max_length=150,
        null=False,
        blank=False,
        unique=True
    )

    email = models.CharField(
        help_text=_('Valid email address for communication purpose'),
        max_length=150,
        null=False,
        blank=False
    )

    Address = models.CharField(
        help_text=_('Address of the organisation/institution'),
        max_length=250,
        null=False,
        blank=False,
    )

    phone = models.CharField(
        help_text=_('Phone number/Landline'),
        max_length=150,
        null=False,
        blank=False
    )

    slug = models.SlugField(unique=True)
    objects = models.Manager()
    approved_objects = ApprovedTrainingCenterManager()
    unapproved_objects = UnapprovedTrainingCenterManager()

    # noinspection PyClassicStyleClass.
    class Meta:
        """ Meta class for training centre. """
        app_label = 'certification'
        ordering = ['name']

    def save(self, *args, **kwargs):
        """ Overloaded save method
        :param args:
        :param kwargs:
        """
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
        """Return URL to training center detail page
        :return: URL
        :rtype: str
        """
        return reverse('training-center-detail', kwargs={'slug': self.slug})


class CourseType(models.Model):
    """ Course Type model """
    name = models.CharField(
        help_text="Course type",
        max_length=200,
        null=False,
        blank=False
    )

    slug = models.SlugField(unique=True)
    objects = models.Manager()
    training_center = models.ManyToManyField(
        TrainingCenter,
        through='Membership',
        through_fields=('coursetype', 'trainingcenter')
    )

    # noinspection PyClassicStyleClass.
    class Meta:
        """ Meta class for Course types """
        app_label = 'certification'
        ordering = ['name']

    def save(self, *args, **kwargs):
        """ Overloaded save method
        :param args:
        :param kwargs:
        """
        if not self.pk:
            words = self.name.split()
            filtered_words = [t for t in words if t.lower() not in STOP_WORDS]
            # unidecode() represents special characters (unicode data) in ASCII
            new_list = unidecode(' '.join(filtered_words))
            self.slug = slugify(new_list)[:50]

        super(CourseType, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s' % self.name


class Membership(models.Model):
    """ Many to many relationship for Course Type and Training Center """
    coursetype = models.ForeignKey(CourseType, on_delete=models.CASCADE)
    trainingcenter = models.ForeignKey(TrainingCenter, on_delete=models.CASCADE)


class CourseConvener(models.Model):
    """ Register Course Convener """
    name = models.CharField(
        help_text="First name of course conveners",
        max_length=150,
        null=False,
        blank=False
    )

    surename = models.CharField(
        help_text="Surename course conveners",
        max_length=150,
        null=False,
        blank=False
    )

    email = models.CharField(
        help_text="Email address",
        max_length=200,
        null=False,
        blank=False
    )

    slug = models.SlugField(unique=True)
    objects = models.Manager()

    # noinspection PyClassicStyleClass.
    class Meta:
        """ Meta class for Course convener """
        app_label = 'certification'
        ordering = ['name']

    def save(self, *args, **kwargs):
        """ Overloaded save method
        :param args:
        :param kwargs:
        """
        if not self.pk:
            words = self.name.split()
            filtered_words = [t for t in words if t.lower() not in STOP_WORDS]
            # unidecode() represents special characters (unicode data) in ASCII
            new_list = unidecode(' '.join(filtered_words))
            self.slug = slugify(new_list)[:50]

        super(CourseConvener, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s' % self.name


class CourseAttendee(models.Model):
    """ Course Attendee model """
    name = models.CharField(
        help_text="First name course attendee",
        max_length=200,
        null=False,
        blank=False
    )

    surename = models.CharField(
        help_text="Surename course attendee",
        max_length=200,
        null=False,
        blank=False
    )

    email = models.CharField(
        help_text="Email address",
        max_length=200,
        null=False,
        blank=False
    )

    slug = models.SlugField(unique=True)
    objects = models.Manager()

    # noinspection PyClassicStyleClass.
    class Meta:
        """ Meta class for Course attendee """
        app_label = 'certification'
        ordering = ['name']

    def save(self, *args, **kwargs):
        """ Overloaded save method
        :param args:
        :param kwargs:
        """
        if not self.pk:
            words = self.name.split()
            filtered_words = [t for t in words if t.lower() not in STOP_WORDS]
            # unidecode() represents special characters (unicode data) in ASCII
            new_list = unidecode(' '.join(filtered_words))
            self.slug = slugify(new_list)[:50]

        super(CourseAttendee, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s' % self.name


class CertifyingOrganisation(models.Model):
    name = models.CharField(
        help_text="Name of Organisation or Institution",
        max_length=200,
        null=False,
        blank=False
    )

    organisation_email = models.CharField(
        help_text="Email address Organisation or Institution",
        max_length=200,
        null=False,
        blank=False
    )

    organisation_phone = models.CharField(
        help_text="Contact of Organisation or Institution",
        max_length=200,
        null=False,
        blank=False
    )

    slug = models.SlugField(unique=True)
    objects = models.Manager()

    # noinspection PyClassicStyleClass.
    class Meta:
        """ Meta class for Course attendee """
        app_label = 'certification'
        ordering = ['name']

    def save(self, *args, **kwargs):
        """ Overloaded save method
        :param args:
        :param kwargs:
        """
        if not self.pk:
            words = self.name.split()
            filtered_words = [t for t in words if t.lower() not in STOP_WORDS]
            # unidecode() represents special characters (unicode data) in ASCII
            new_list = unidecode(' '.join(filtered_words))
            self.slug = slugify(new_list)[:50]

        super(CertifyingOrganisation, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s' % self.name


class Certificate(models.Model):
    student = models.ForeignKey(CourseAttendee, on_delete=models.CASCADE)