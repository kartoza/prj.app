# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Committee'
        db.create_table(u'vota_committee', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetime_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('datetime_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('creator', self.gf('threaded_multihost.fields.CreatorField')(default=None, related_name='committee_created', null=True, blank=True, to=orm['auth.User'])),
            ('editor', self.gf('threaded_multihost.fields.EditorField')(blank=True, related_name='committee_last_modified', null=True, to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('sort_number', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('quorum_setting', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.Project'])),
        ))
        db.send_create_signal('vota', ['Committee'])

        # Adding unique constraint on 'Committee', fields ['name', 'project']
        db.create_unique(u'vota_committee', ['name', 'project_id'])

        # Adding M2M table for field users on 'Committee'
        m2m_table_name = db.shorten_name(u'vota_committee_users')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('committee', models.ForeignKey(orm['vota.committee'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['committee_id', 'user_id'])

        # Adding model 'Ballot'
        db.create_table(u'vota_ballot', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetime_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('datetime_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('creator', self.gf('threaded_multihost.fields.CreatorField')(default=None, related_name='ballot_created', null=True, blank=True, to=orm['auth.User'])),
            ('editor', self.gf('threaded_multihost.fields.EditorField')(blank=True, related_name='ballot_last_modified', null=True, to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=3000)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('denied', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('no_quorum', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('committee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vota.Committee'])),
        ))
        db.send_create_signal('vota', ['Ballot'])

        # Adding unique constraint on 'Ballot', fields ['name', 'committee']
        db.create_unique(u'vota_ballot', ['name', 'committee_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Ballot', fields ['name', 'committee']
        db.delete_unique(u'vota_ballot', ['name', 'committee_id'])

        # Removing unique constraint on 'Committee', fields ['name', 'project']
        db.delete_unique(u'vota_committee', ['name', 'project_id'])

        # Deleting model 'Committee'
        db.delete_table(u'vota_committee')

        # Removing M2M table for field users on 'Committee'
        db.delete_table(db.shorten_name(u'vota_committee_users'))

        # Deleting model 'Ballot'
        db.delete_table(u'vota_ballot')


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
        'base.project': {
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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'vota.ballot': {
            'Meta': {'unique_together': "(('name', 'committee'),)", 'object_name': 'Ballot'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'committee': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vota.Committee']"}),
            'creator': ('threaded_multihost.fields.CreatorField', [], {'default': 'None', 'related_name': "'ballot_created'", 'null': 'True', 'blank': 'True', 'to': u"orm['auth.User']"}),
            'datetime_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'datetime_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'denied': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '3000'}),
            'editor': ('threaded_multihost.fields.EditorField', [], {'blank': 'True', 'related_name': "'ballot_last_modified'", 'null': 'True', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'no_quorum': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'vota.committee': {
            'Meta': {'unique_together': "(('name', 'project'),)", 'object_name': 'Committee'},
            'creator': ('threaded_multihost.fields.CreatorField', [], {'default': 'None', 'related_name': "'committee_created'", 'null': 'True', 'blank': 'True', 'to': u"orm['auth.User']"}),
            'datetime_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'datetime_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'editor': ('threaded_multihost.fields.EditorField', [], {'blank': 'True', 'related_name': "'committee_last_modified'", 'null': 'True', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.Project']"}),
            'quorum_setting': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'sort_number': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['vota']