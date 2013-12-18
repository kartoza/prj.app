# -*- coding: utf-8 -*-
import datetime
from django.utils.text import slugify
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from django.db import transaction


class Migration(SchemaMigration):

    def forwards(self, orm):
        with transaction.atomic():
            # Adding field 'Version.slug'
            db.add_column(u'changes_version', 'slug',
                          self.gf('django.db.models.fields.SlugField')(blank=True, null=True, unique=False, max_length=50),
                          keep_default=False)

            # Adding field 'Entry.slug'
            db.add_column(u'changes_entry', 'slug',
                          self.gf('django.db.models.fields.SlugField')(
                              blank=True, null=True, unique=False, max_length=50),
                          keep_default=False)

            # Adding field 'Category.slug'
            db.add_column(u'changes_category', 'slug',
                          self.gf('django.db.models.fields.SlugField')(
                              blank=True, null=True, unique=False, max_length=50),
                          keep_default=False)

        with transaction.atomic():
            objects = orm['changes.Category'].objects.all()
            for obj in objects:
                obj.slug = slugify(obj.name)
                obj.save()

            objects = orm['changes.Version'].objects.all()
            for obj in objects:
                obj.slug = slugify(obj.name)
                obj.save()

            objects = orm['changes.Entry'].objects.all()
            for obj in objects:
                stop_words = (
                    'a', 'an', 'and', 'if', 'is', 'the', 'in', 'i', 'you', 'other',
                    'this', 'that'
                )
                words = obj.title.split()
                filtered_words = [t for t in words if t.lower() not in stop_words]
                new_list = ' '.join(filtered_words)
                obj.slug = slugify(new_list)[:49]
                obj.save()


    def backwards(self, orm):
        # Deleting field 'Version.slug'
        db.delete_column(u'changes_version', 'slug')

        # Deleting field 'Entry.slug'
        db.delete_column(u'changes_entry', 'slug')

        # Deleting field 'Category.slug'
        db.delete_column(u'changes_category', 'slug')


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
            'Meta': {'ordering': "['name']", 'object_name': 'Project'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'creator': ('threaded_multihost.fields.CreatorField', [], {'default': 'None', 'related_name': "'project_created'", 'null': 'True', 'blank': 'True', 'to': u"orm['auth.User']"}),
            'datetime_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'datetime_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'editor': ('threaded_multihost.fields.EditorField', [], {'blank': 'True', 'related_name': "'project_last_modified'", 'null': 'True', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        'changes.category': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('name', 'project'),)", 'object_name': 'Category'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'creator': ('threaded_multihost.fields.CreatorField', [], {'default': 'None', 'related_name': "'category_created'", 'null': 'True', 'blank': 'True', 'to': u"orm['auth.User']"}),
            'datetime_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'datetime_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'editor': ('threaded_multihost.fields.EditorField', [], {'blank': 'True', 'related_name': "'category_last_modified'", 'null': 'True', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.Project']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'sort_number': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'})
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
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'version': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['changes.Version']"})
        },
        'changes.version': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('name', 'project'),)", 'object_name': 'Version'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'creator': ('threaded_multihost.fields.CreatorField', [], {'default': 'None', 'related_name': "'version_created'", 'null': 'True', 'blank': 'True', 'to': u"orm['auth.User']"}),
            'datetime_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'datetime_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'editor': ('threaded_multihost.fields.EditorField', [], {'blank': 'True', 'related_name': "'version_last_modified'", 'null': 'True', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.Project']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
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
