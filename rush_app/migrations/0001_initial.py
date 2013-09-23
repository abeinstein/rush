# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Rush'
        db.create_table(u'rush_app_rush', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=15, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('bid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('last_commented', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('frat', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rush_app.Frat'])),
            ('dorm', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('hometown', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'rush_app', ['Rush'])

        # Adding model 'Frat'
        db.create_table(u'rush_app_frat', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('chapter', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('university', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'rush_app', ['Frat'])

        # Adding unique constraint on 'Frat', fields ['name', 'chapter']
        db.create_unique(u'rush_app_frat', ['name', 'chapter'])

        # Adding model 'UserProfile'
        db.create_table(u'rush_app_userprofile', (
            ('about_me', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('facebook_id', self.gf('django.db.models.fields.BigIntegerField')(unique=True, null=True, blank=True)),
            ('access_token', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('facebook_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('facebook_profile_url', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('website_url', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('blog_url', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('date_of_birth', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('raw_data', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('facebook_open_graph', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('new_token_required', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=255, null=True, blank=True)),
            ('user', self.gf('annoying.fields.AutoOneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('frat', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rush_app.Frat'])),
            ('is_admin', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'rush_app', ['UserProfile'])

        # Adding model 'Reputation'
        db.create_table(u'rush_app_reputation', (
            ('rush', self.gf('annoying.fields.AutoOneToOneField')(to=orm['rush_app.Rush'], unique=True, primary_key=True)),
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

        # Adding model 'Comment'
        db.create_table(u'rush_app_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('rush', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rush_app.Rush'])),
            ('userprofile', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rush_app.UserProfile'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'rush_app', ['Comment'])


    def backwards(self, orm):
        # Removing unique constraint on 'Frat', fields ['name', 'chapter']
        db.delete_unique(u'rush_app_frat', ['name', 'chapter'])

        # Deleting model 'Rush'
        db.delete_table(u'rush_app_rush')

        # Deleting model 'Frat'
        db.delete_table(u'rush_app_frat')

        # Deleting model 'UserProfile'
        db.delete_table(u'rush_app_userprofile')

        # Deleting model 'Reputation'
        db.delete_table(u'rush_app_reputation')

        # Removing M2M table for field thumbsup_users on 'Reputation'
        db.delete_table(db.shorten_name(u'rush_app_reputation_thumbsup_users'))

        # Removing M2M table for field thumbsdown_users on 'Reputation'
        db.delete_table(db.shorten_name(u'rush_app_reputation_thumbsdown_users'))

        # Deleting model 'Comment'
        db.delete_table(u'rush_app_comment')


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
            'about_me': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'access_token': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'blog_url': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'facebook_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'facebook_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'facebook_open_graph': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'facebook_profile_url': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'frat': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['rush_app.Frat']"}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'new_token_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'raw_data': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('annoying.fields.AutoOneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'}),
            'website_url': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['rush_app']