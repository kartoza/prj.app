"""
This model is to create "ballots" i.e. questions/proposals/changes which a
Committee can vote on to either Pass or Deny.


"""
import logging

from django.db import models
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


VOTE_CHOICES = (
    ('y', 'Yes'),
    ('-', 'Abstain'),
    ('n', 'No')
)


class Vote(models.Model):
    """A vote model."""

    choice = models.CharField(max_length=1, choices=VOTE_CHOICES,
                              default='-')
    user = models.ForeignKey(User)
    # noinspection PyUnresolvedReferences
    ballot = models.ForeignKey('Ballot')
    objects = models.Manager()

    # noinspection PyClassicStyleClass
    class Meta:
        """Meta options for the vote class."""
        unique_together = ('user', 'ballot')
        app_label = 'vota'

    def __unicode__(self):
        return u'%s : %s' % (self.ballot.name, self.user.username)
