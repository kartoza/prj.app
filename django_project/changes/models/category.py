import logging
logger = logging.getLogger(__name__)
from django.db import models
from audited_models.models import AuditedModel


class ApprovedCategoryManager(models.Manager):
    """Custom category manager that shows only approved records."""

    def get_query_set(self):
        """Query set generator"""
        return super(
            ApprovedCategoryManager, self).get_query_set().filter(
                approved=True)


class UnapprovedCategoryManager(models.Manager):
    """Custom version manager that shows only unapproved records."""

    def get_query_set(self):
        """Query set generator"""
        return super(
            UnapprovedCategoryManager, self).get_query_set().filter(
                approved=False)


class Category(AuditedModel):
    """A category model e.g. gui, backend, web site etc."""
    name = models.CharField(
        help_text='Name of this category.',
        max_length=255,
        null=False,
        blank=False,
        unique=True)

    approved = models.BooleanField(
        help_text=(
            'Whether this version has been approved for use by the '
            'project owner.'),
        default=False
    )

    project = models.ForeignKey('Project')

    objects = ApprovedCategoryManager()
    all_objects = models.Manager()
    unapproved_objects = UnapprovedCategoryManager()

    class Meta:
        """Meta options for the category class."""
        unique_together = ('name', 'project')
        app_label = 'changes'

    def __unicode__(self):
        return u'%s' % self.name
