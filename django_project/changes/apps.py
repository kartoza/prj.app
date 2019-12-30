"""
Auto generated file when creating changes app.
"""


from __future__ import unicode_literals

from django.apps import AppConfig
from django.db.models.signals import post_migrate
from changes.signals.handlers import create_notice_types


class ChangesConfig(AppConfig):
    """Auto-generated application configurations."""
    name = 'changes'
    verbose_name = 'Changes'

    def ready(self):
        post_migrate.connect(create_notice_types, sender=self)
