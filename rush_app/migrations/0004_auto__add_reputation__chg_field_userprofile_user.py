# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Reputation'
        db.create_table(u'rush_app_reputation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rush', self.gf('annoying.fields.AutoOneToOneField')(to=orm['rush_app.Rush'], unique=True)),
            ('thumbsup', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('thumbsdown', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'rush_app', ['Reputation'])

        # Adding M2M table for field thumbsup_users on 'Reputation'
        m2m_table_name = db.shorten_name(u'rush_app_reputation_thumbsup_users')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('reputation', models.ForeignKey(orm[u'rush_app.reputation'], null=False)),
            ('userprofile', models.ForeignKey(orm[u'rush_app.userprofile'], null=False))
        ))
        db.create_unique(m2m_table_name, ['reputation_id', 'userprofile_id'])

        # Adding M2M table for field thumbsdown_users on 'Reputation'
        m2m_table_name = db.shorten_name(u'rush_app_reputation_thumbsdown_users')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('reputation', models.ForeignKey(orm[u'rush_app.reputation'], null=False)),
            ('userprofile', models.ForeignKey(orm[u'rush_app.userprofile'], null=False))
        ))
        db.create_unique(m2m_table_name, ['reputation_id', 'userprofile_id'])


        # Changing field 'UserProfile.user'
        db.alter_column(u'rush_app_userprofile', 'user_id', self.gf('annoying.fields.AutoOneToOneField')(to=orm['auth.User'], unique=True))

    def backwards(self, orm):
        # Deleting model 'Reputation'
        db.delete_table(u'rush_app_reputation')

        # Removing M2M table for field thumbsup_users on 'Reputation'
        db.delete_table(db.shorten_name(u'rush_app_reputation_thumbsup_users'))

        # Removing M2M table for field thumbsdown_users on 'Reputation'
        db.delete_table(db.shorten_name(u'rush_app_reputation_thumbsdown_users'))


        # Changing field 'UserProfile.user'
        db.alter_column(u'rush_app_userprofile', 'user_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True))

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
        u'rush_app.frat': {
            'Meta': {'object_name': 'Frat'},
            'chapter': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'university': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'rush_app.reputation': {
            'Meta': {'object_name': 'Reputation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rush': ('annoying.fields.AutoOneToOneField', [], {'to': u"orm['rush_app.Rush']", 'unique': 'True'}),
            'thumbsdown': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'thumbsdown_users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'td+'", 'symmetrical': 'False', 'to': u"orm['rush_app.UserProfile']"}),
            'thumbsup': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'thumbsup_users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'tu+'", 'symmetrical': 'False', 'to': u"orm['rush_app.UserProfile']"})
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
            'last_commented': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'picture': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'rush_app.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'frat': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['rush_app.Frat']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('annoying.fields.AutoOneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['rush_app']