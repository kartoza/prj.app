__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '26/02/18'

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    qualifications = models.CharField(
        max_length=250,
        blank=True,
        default=''
    )
    other = models.CharField(
        max_length=100,
        blank=True,
        default=''
    )

    class Meta:
        app_label = 'base'

    def __unicode__(self):
        return u'%s' % self.qualifications
