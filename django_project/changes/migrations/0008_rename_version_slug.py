# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration:

    def forwards(self, orm):
        db.rename_column('changes_version', 'slug', 'version_slug')


    def backwards(self, orm):
        db.rename_column('changes_version', 'version_slug', 'slug')
