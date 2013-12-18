import datetime
from django.utils.text import slugify
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from django.db import transaction


class Migration(SchemaMigration):
    def forwards(self, orm):
        with transaction.atomic():
            db.create_unique(u'changes_category', ['slug'])
            db.create_unique(u'changes_version', ['slug'])
            db.create_unique(u'changes_entry', ['slug'])

    def backwards(self, orm):
        db.delete_unique(u'changes_category', ['slug'])
        db.delete_unique(u'changes_version', ['slug'])
        db.delete_unique(u'changes_entry', ['slug'])
