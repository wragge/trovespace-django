# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Page.checksum'
        db.add_column(u'trovetraces_page', 'checksum',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=250),
                      keep_default=False)


        # Changing field 'Page.domain'
        db.alter_column(u'trovetraces_page', 'domain', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

        # Changing field 'Page.url'
        db.alter_column(u'trovetraces_page', 'url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True))

        # Changing field 'Page.file_id'
        db.alter_column(u'trovetraces_page', 'file_id', self.gf('django.db.models.fields.CharField')(max_length=250, null=True))

        # Changing field 'Page.tld'
        db.alter_column(u'trovetraces_page', 'tld', self.gf('django.db.models.fields.CharField')(max_length=20, null=True))

    def backwards(self, orm):
        # Deleting field 'Page.checksum'
        db.delete_column(u'trovetraces_page', 'checksum')


        # Changing field 'Page.domain'
        db.alter_column(u'trovetraces_page', 'domain', self.gf('django.db.models.fields.CharField')(default=1, max_length=100))

        # Changing field 'Page.url'
        db.alter_column(u'trovetraces_page', 'url', self.gf('django.db.models.fields.URLField')(default=1, max_length=200))

        # Changing field 'Page.file_id'
        db.alter_column(u'trovetraces_page', 'file_id', self.gf('django.db.models.fields.CharField')(default=1, max_length=250))

        # Changing field 'Page.tld'
        db.alter_column(u'trovetraces_page', 'tld', self.gf('django.db.models.fields.CharField')(default=1, max_length=20))

    models = {
        u'trovetraces.article': {
            'Meta': {'object_name': 'Article'},
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'newspaper_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'newspaper_title': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'page': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'trovetraces.backlink': {
            'Meta': {'object_name': 'Backlink'},
            'anchor': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'context': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'href': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trovetraces.Page']", 'null': 'True', 'blank': 'True'}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trovetraces.Article']", 'null': 'True', 'blank': 'True'})
        },
        u'trovetraces.page': {
            'Meta': {'object_name': 'Page'},
            'checksum': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'cleaned_html': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'file_id': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page_title': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'tld': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['trovetraces']