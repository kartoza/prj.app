__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '19/07/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'

import logging

logger = logging.getLogger(__name__)
from django.contrib.auth.models import User
from django.db import models


class ProjectAdministrator(models.Model):
    """A category model e.g. gui, backend, web site etc."""
    project = models.ForeignKey('base.Project')
    user = models.ForeignKey(User)

    # noinspection PyClassicStyleClass
    class Meta:
        """Meta options for the category class."""
        unique_together = (
            ('project', 'user')
        )
        app_label = 'permission'
        ordering = ['project', 'user']

    def save(self, *args, **kwargs):
        super(ProjectAdministrator, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s : %s' % (self.project.name, self.user.username)
