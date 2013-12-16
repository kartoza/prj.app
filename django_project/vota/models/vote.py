"""
This model is to create "ballots" i.e. questions/proposals/changes which a
Committee can vote on to either Pass or Deny.


"""
import logging

logger = logging.getLogger(__name__)
from django.db import models
from audited_models.models import AuditedModel
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class Vote(AuditedModel):
    """A vote model"""

    positive = models.BooleanField(
        help_text=_('A yes, or +1 from the committee member'),
        default=False
    )

    abstain = models.BooleanField(
        help_text=_('Whether the committee member abstained'),
        default=False
    )

    negative = models.BooleanField(
        help_text=_('A No, or -1 from the committee member'),
        default=False
    )

    user = models.ForeignKey(User)
    # noinspection PyUnresolvedReferences
    ballot = models.ForeignKey('Ballot')
    objects = models.Manager()

    class Meta:
        """Meta options for the vote class."""
        unique_together = ('user', 'ballot')
        app_label = 'vota'

    def __unicode__(self):
        return u'%s : %s' % (self.project.name, self.name)
