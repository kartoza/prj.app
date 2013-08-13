# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'changes_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetime_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('datetime_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('creator', self.gf('threaded_multihost.fields.CreatorField')(default=None, related_name='category_created', null=True, blank=True, to=orm['auth.User'])),
            ('editor', self.gf('threaded_multihost.fields.EditorField')(blank=True, related_name='category_last_modified', null=True, to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['changes.Project'])),
        ))
        db.send_create_signal('changes', ['Category'])

        # Adding unique constraint on 'Category', fields ['name', 'project']
        db.create_unique(u'changes_category', ['name', 'project_id'])

        # Adding model 'Entry'
        db.create_table(u'changes_entry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetime_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('datetime_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('creator', self.gf('threaded_multihost.fields.CreatorField')(default=None, related_name='entry_created', null=True, blank=True, to=orm['auth.User'])),
            ('editor', self.gf('threaded_multihost.fields.EditorField')(blank=True, related_name='entry_last_modified', null=True, to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('image_file', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('image_credits', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('version', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['changes.Version'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['changes.Category'])),
        ))
        db.send_create_signal('changes', ['Entry'])

        # Adding unique constraint on 'Entry', fields ['title', 'version', 'category']
        db.create_unique(u'changes_entry', ['title', 'version_id', 'category_id'])

        # Adding model 'Version'
        db.create_table(u'changes_version', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetime_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('datetime_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('creator', self.gf('threaded_multihost.fields.CreatorField')(default=None, related_name='version_created', null=True, blank=True, to=orm['auth.User'])),
            ('editor', self.gf('threaded_multihost.fields.EditorField')(blank=True, related_name='version_last_modified', null=True, to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('image_file', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['changes.Project'])),
        ))
        db.send_create_signal('changes', ['Version'])

        # Adding unique constraint on 'Version', fields ['name', 'project']
        db.create_unique(u'changes_version', ['name', 'project_id'])

        # Adding model 'Project'
        db.create_table(u'changes_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetime_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('datetime_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('creator', self.gf('threaded_multihost.fields.CreatorField')(default=None, related_name='project_created', null=True, blank=True, to=orm['auth.User'])),
            ('editor', self.gf('threaded_multihost.fields.EditorField')(blank=True, related_name='project_last_modified', null=True, to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('image_file', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('changes', ['Project'])


    def backwards(self, orm):
        # Removing unique constraint on 'Version', fields ['name', 'project']
        db.delete_unique(u'changes_version', ['name', 'project_id'])

        # Removing unique constraint on 'Entry', fields ['title', 'version', 'category']
        db.delete_unique(u'changes_entry', ['title', 'version_id', 'category_id'])

        # Removing unique constraint on 'Category', fields ['name', 'project']
        db.delete_unique(u'changes_category', ['name', 'project_id'])

        # Deleting model 'Category'
        db.delete_table(u'changes_category')

        # Deleting model 'Entry'
        db.delete_table(u'changes_entry')

        # Deleting model 'Version'
        db.delete_table(u'changes_version')

        # Deleting model 'Project'
        db.delete_table(u'changes_project')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'changes.category': {
            'Meta': {'unique_together': "(('name', 'project'),)", 'object_name': 'Category'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'creator': ('threaded_multihost.fields.CreatorField', [], {'default': 'None', 'related_name': "'category_created'", 'null': 'True', 'blank': 'True', 'to': u"orm['auth.User']"}),
            'datetime_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'datetime_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'editor': ('threaded_multihost.fields.EditorField', [], {'blank': 'True', 'related_name': "'category_last_modified'", 'null': 'True', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['changes.Project']"})
        },
        'changes.entry': {
            'Meta': {'unique_together': "(('title', 'version', 'category'),)", 'object_name': 'Entry'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['changes.Category']"}),
            'creator': ('threaded_multihost.fields.CreatorField', [], {'default': 'None', 'related_name': "'entry_created'", 'null': 'True', 'blank': 'True', 'to': u"orm['auth.User']"}),
            'datetime_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'datetime_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'editor': ('threaded_multihost.fields.EditorField', [], {'blank': 'True', 'related_name': "'entry_last_modified'", 'null': 'True', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_credits': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image_file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'version': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['changes.Version']"})
        },
        'changes.project': {
            'Meta': {'object_name': 'Project'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'creator': ('threaded_multihost.fields.CreatorField', [], {'default': 'None', 'related_name': "'project_created'", 'null': 'True', 'blank': 'True', 'to': u"orm['auth.User']"}),
            'datetime_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'datetime_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'editor': ('threaded_multihost.fields.EditorField', [], {'blank': 'True', 'related_name': "'project_last_modified'", 'null': 'True', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'changes.version': {
            'Meta': {'unique_together': "(('name', 'project'),)", 'object_name': 'Version'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'creator': ('threaded_multihost.fields.CreatorField', [], {'default': 'None', 'related_name': "'version_created'", 'null': 'True', 'blank': 'True', 'to': u"orm['auth.User']"}),
            'datetime_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'datetime_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'editor': ('threaded_multihost.fields.EditorField', [], {'blank': 'True', 'related_name': "'version_last_modified'", 'null': 'True', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['changes.Project']"})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['changes']