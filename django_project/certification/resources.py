# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from import_export import resources
from .models.attendee import Attendee

class AttendeeModelResource(resources.ModelResource):
    """Resource for admin csv import and export."""
    class Meta:
        model = Attendee
