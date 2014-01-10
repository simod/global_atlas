# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Map'
        db.create_table(u'maps_map', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('theme', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['maps.Theme'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['maps.Category'])),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['maps.Source'])),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('scale', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('request', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['maps.MapRequest'])),
            ('map_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('map_thumbnail', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('center', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['maps.Country'])),
            ('size', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['maps.MapSize'], null=True, blank=True)),
        ))
        db.send_create_signal(u'maps', ['Map'])

        # Adding model 'Theme'
        db.create_table(u'maps_theme', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
        ))
        db.send_create_signal(u'maps', ['Theme'])

        # Adding model 'MapRequest'
        db.create_table(u'maps_maprequest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('date', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('purpose', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('extended_description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('size', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['maps.MapSize'])),
            ('format', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['maps.Format'])),
            ('requester', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['maps.Requester'])),
        ))
        db.send_create_signal(u'maps', ['MapRequest'])

        # Adding model 'Country'
        db.create_table(u'maps_country', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fips', self.gf('django.db.models.fields.CharField')(unique=True, max_length=5)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('iso2', self.gf('django.db.models.fields.CharField')(max_length=2, unique=True, null=True, blank=True)),
            ('iso3', self.gf('django.db.models.fields.CharField')(max_length=3, unique=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'maps', ['Country'])

        # Adding M2M table for field countries on 'Country'
        m2m_table_name = db.shorten_name(u'maps_country_countries')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_country', models.ForeignKey(orm[u'maps.country'], null=False)),
            ('to_country', models.ForeignKey(orm[u'maps.country'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_country_id', 'to_country_id'])

        # Adding model 'Format'
        db.create_table(u'maps_format', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('resolution', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'maps', ['Format'])

        # Adding unique constraint on 'Format', fields ['name', 'resolution']
        db.create_unique(u'maps_format', ['name', 'resolution'])

        # Adding model 'MapSize'
        db.create_table(u'maps_mapsize', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=5)),
            ('dimensions', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
        ))
        db.send_create_signal(u'maps', ['MapSize'])

        # Adding model 'Category'
        db.create_table(u'maps_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
        ))
        db.send_create_signal(u'maps', ['Category'])

        # Adding model 'Requester'
        db.create_table(u'maps_requester', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
        ))
        db.send_create_signal(u'maps', ['Requester'])

        # Adding model 'Source'
        db.create_table(u'maps_source', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
        ))
        db.send_create_signal(u'maps', ['Source'])


    def backwards(self, orm):
        # Removing unique constraint on 'Format', fields ['name', 'resolution']
        db.delete_unique(u'maps_format', ['name', 'resolution'])

        # Deleting model 'Map'
        db.delete_table(u'maps_map')

        # Deleting model 'Theme'
        db.delete_table(u'maps_theme')

        # Deleting model 'MapRequest'
        db.delete_table(u'maps_maprequest')

        # Deleting model 'Country'
        db.delete_table(u'maps_country')

        # Removing M2M table for field countries on 'Country'
        db.delete_table(db.shorten_name(u'maps_country_countries'))

        # Deleting model 'Format'
        db.delete_table(u'maps_format')

        # Deleting model 'MapSize'
        db.delete_table(u'maps_mapsize')

        # Deleting model 'Category'
        db.delete_table(u'maps_category')

        # Deleting model 'Requester'
        db.delete_table(u'maps_requester')

        # Deleting model 'Source'
        db.delete_table(u'maps_source')


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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'maps.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'maps.country': {
            'Meta': {'object_name': 'Country'},
            'countries': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['maps.Country']", 'null': 'True', 'blank': 'True'}),
            'fips': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso2': ('django.db.models.fields.CharField', [], {'max_length': '2', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'iso3': ('django.db.models.fields.CharField', [], {'max_length': '3', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        u'maps.format': {
            'Meta': {'unique_together': "(('name', 'resolution'),)", 'object_name': 'Format'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'resolution': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'maps.map': {
            'Meta': {'object_name': 'Map'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['maps.Category']"}),
            'center': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['maps.Country']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'map_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'map_thumbnail': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'request': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['maps.MapRequest']"}),
            'scale': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'size': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['maps.MapSize']", 'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['maps.Source']"}),
            'theme': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['maps.Theme']"}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        u'maps.maprequest': {
            'Meta': {'object_name': 'MapRequest'},
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'extended_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'format': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['maps.Format']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'purpose': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'requester': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['maps.Requester']"}),
            'size': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['maps.MapSize']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'maps.mapsize': {
            'Meta': {'object_name': 'MapSize'},
            'dimensions': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'})
        },
        u'maps.requester': {
            'Meta': {'object_name': 'Requester'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'maps.source': {
            'Meta': {'object_name': 'Source'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'maps.theme': {
            'Meta': {'object_name': 'Theme'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        }
    }

    complete_apps = ['maps']