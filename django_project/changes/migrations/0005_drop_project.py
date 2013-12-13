# Project model moved to base app

import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    depends_on = (
        ('base', '0002_create_project'),
    )
    def forwards(self, orm):
        pass

    def backwards(self, orm):
        pass
