__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '17/05/18'

from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Payment(models.Model):
    """Model to save payment of user."""

    user = models.ForeignKey(User)
    model_id = models.IntegerField()
    model_name = models.CharField(
        max_length=32)
    model_app_label = models.CharField(
        max_length=32)
    payment_id = models.CharField(
        max_length=32)
    time_transaction = models.DateTimeField(
        default=datetime.now)
    amount = models.FloatField(
        help_text=_('This is amount of money user paid.'))
    currency = models.CharField(
        max_length=4)
    description = models.CharField(
        max_length=126)
    note = models.CharField(
        max_length=32,
        null=True,
        blank=True)

    def __unicode__(self):
        return self.payment_id
