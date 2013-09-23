# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'UserProfile.access_token'
        db.delete_column(u'rush_app_userprofile', 'access_token')

        # Deleting field 'UserProfile.gender'
        db.delete_column(u'rush_app_userprofile', 'gender')

        # Deleting field 'UserProfile.image'
        db.delete_column(u'rush_app_userprofile', 'image')

        # Deleting field 'UserProfile.facebook_name'
        db.delete_column(u'rush_app_userprofile', 'facebook_name')

        # Deleting field 'UserProfile.raw_data'
        db.delete_column(u'rush_app_userprofile', 'raw_data')

        # Deleting field 'UserProfile.date_of_birth'
        db.delete_column(u'rush_app_userprofile', 'date_of_birth')

        # Deleting field 'UserProfile.about_me'
        db.delete_column(u'rush_app_userprofile', 'about_me')

        # Deleting field 'UserProfile.blog_url'
        db.delete_column(u'rush_app_userprofile', 'blog_url')

        # Deleting field 'UserProfile.facebook_id'
        db.delete_column(u'rush_app_userprofile', 'facebook_id')

        # Deleting field 'UserProfile.facebook_open_graph'
        db.delete_column(u'rush_app_userprofile', 'facebook_open_graph')

        # Deleting field 'UserProfile.new_token_required'
        db.delete_column(u'rush_app_userprofile', 'new_token_required')

        # Deleting field 'UserProfile.facebook_profile_url'
        db.delete_column(u'rush_app_userprofile', 'facebook_profile_url')

        # Deleting field 'UserProfile.website_url'
        db.delete_column(u'rush_app_userprofile', 'website_url')


        # Changing field 'UserProfile.frat'
        db.alter_column(u'rush_app_userprofile', 'frat_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rush_app.Frat'], null=True))

    def backwards(self, orm):
        # Adding field 'UserProfile.access_token'
        db.add_column(u'rush_app_userprofile', 'access_token',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'UserProfile.gender'
        db.add_column(u'rush_app_userprofile', 'gender',
                      self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True),
                      keep_default=False)

        # Adding field 'UserProfile.image'
        db.add_column(u'rush_app_userprofile', 'image',
                      self.gf('django.db.models.fields.files.ImageField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'UserProfile.facebook_name'
        db.add_column(u'rush_app_userprofile', 'facebook_name',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'UserProfile.raw_data'
        db.add_column(u'rush_app_userprofile', 'raw_data',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'UserProfile.date_of_birth'
        db.add_column(u'rush_app_userprofile', 'date_of_birth',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'UserProfile.about_me'
        db.add_column(u'rush_app_userprofile', 'about_me',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'UserProfile.blog_url'
        db.add_column(u'rush_app_userprofile', 'blog_url',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'UserProfile.facebook_id'
        db.add_column(u'rush_app_userprofile', 'facebook_id',
                      self.gf('django.db.models.fields.BigIntegerField')(unique=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'UserProfile.facebook_open_graph'
        db.add_column(u'rush_app_userprofile', 'facebook_open_graph',
                      self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'UserProfile.new_token_required'
        db.add_column(u'rush_app_userprofile', 'new_token_required',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'UserProfile.facebook_profile_url'
        db.add_column(u'rush_app_userprofile', 'facebook_profile_url',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'UserProfile.website_url'
        db.add_column(u'rush_app_userprofile', 'website_url',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'UserProfile.frat'
        raise RuntimeError("Cannot reverse this migration. 'UserProfile.frat' and its values cannot be restored.")

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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'rush_app.comment': {
            'Meta': {'object_name': 'Comment'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rush': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['rush_app.Rush']"}),
            'userprofile': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['rush_app.UserProfile']"})
        },
        u'rush_app.frat': {
            'Meta': {'unique_together': "(('name', 'chapter'),)", 'object_name': 'Frat'},
            'chapter': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'university': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'rush_app.reputation': {
            'Meta': {'object_name': 'Reputation'},
            'rush': ('annoying.fields.AutoOneToOneField', [], {'to': u"orm['rush_app.Rush']", 'unique': 'True', 'primary_key': 'True'}),
            'thumbsdown': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'thumbsdown_users': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'td+'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['rush_app.UserProfile']"}),
            'thumbsup': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'thumbsup_users': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'tu+'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['rush_app.UserProfile']"})
        },
        u'rush_app.rush': {
            'Meta': {'object_name': 'Rush'},
            'bid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dorm': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'frat': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['rush_app.Frat']"}),
            'hometown': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_commented': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'rush_app.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'frat': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['rush_app.Frat']", 'null': 'True', 'blank': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('annoying.fields.AutoOneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['rush_app']