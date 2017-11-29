# coding=utf-8
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
import os


ROLE = (
    ('project', 'project'),
    ('organisation', 'organisation'),
)


class CustomDomain(models.Model):
    """Model to save subscribed user and their custom domain."""

    user = models.ForeignKey(User)
    role = models.CharField(
        choices=ROLE,
        default='project',
        blank=False,
        null=False,
        max_length=30
    )
    custom_domain = models.CharField(
        help_text=_('Custom domain, i.e. www.kartoza.com'),
        max_length=30,
        null=True,
        blank=True
    )
    approved = models.BooleanField(
        help_text=_('Whether this user domain has been approved for use yet.'),
        default=False
    )

    class Meta:
        ordering = ['user']
        unique_together = ['user', 'custom_domain']

    def save(self, *args, **kwargs):
        # update the server_name variable for nginx
        with open('/home/web/media/server-name.txt', 'w') as f:
            f.write('server_name ')
            if not self.pk:
                for domain in CustomDomain.objects.filter(approved=True):
                    f.write(domain.custom_domain + ' ')
            else:
                for query in CustomDomain.objects.filter(
                        approved=True).exclude(pk=self.pk):
                    f.write(query.custom_domain + ' ')
            if self.approved:
                f.write(self.custom_domain + ' ')
            f.write(';')
        super(CustomDomain, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'{}: {}'.format(self.user, self.custom_domain)
