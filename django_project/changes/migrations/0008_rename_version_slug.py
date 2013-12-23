# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration:

    def forwards(self, orm):
        # Rename 'name' field to 'full_name'
        db.rename_column('changes_version', 'slug', 'version_slug')


    def backwards(self, orm):
        # Rename 'full_name' field to 'name'
        db.rename_column('changes_version', 'version_slug', 'slug')
