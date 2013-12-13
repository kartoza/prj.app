import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        db.rename_table('changes_project', 'base_project')

        if not db.dry_run:
            # For permissions to work properly after migrating
            # Does not work for me - Tim
            #orm['contenttypes.ContentType'].objects.filter(
            #    app_label='changes', model='project').update(app_label='base')

            # So I used a raw query update.
            db.execute(
                "update django_content_type set app_label = 'base' where "
                " app_label = 'changes' and model = 'project';")

    def backwards(self, orm):
        db.rename_table('base_project', 'changes_project')

        if not db.dry_run:
            db.execute(
                "update django_content_type set app_label = 'changes' where "
                " app_label = 'base' and model = 'project';")
