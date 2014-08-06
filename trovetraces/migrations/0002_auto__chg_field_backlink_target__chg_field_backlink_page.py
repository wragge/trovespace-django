# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Backlink.target'
        db.alter_column(u'trovetraces_backlink', 'target_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trovetraces.Article'], null=True))

        # Changing field 'Backlink.page'
        db.alter_column(u'trovetraces_backlink', 'page_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trovetraces.Page'], null=True))

    def backwards(self, orm):

        # Changing field 'Backlink.target'
        db.alter_column(u'trovetraces_backlink', 'target_id', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['trovetraces.Article']))

        # Changing field 'Backlink.page'
        db.alter_column(u'trovetraces_backlink', 'page_id', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['trovetraces.Page']))

    models = {
        u'trovetraces.article': {
            'Meta': {'object_name': 'Article'},
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'newspaper_id': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'newspaper_title': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'page': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'trovetraces.backlink': {
            'Meta': {'object_name': 'Backlink'},
            'anchor': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'context': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'href': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trovetraces.Page']", 'null': 'True', 'blank': 'True'}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trovetraces.Article']", 'null': 'True', 'blank': 'True'})
        },
        u'trovetraces.page': {
            'Meta': {'object_name': 'Page'},
            'cleaned_html': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'file_id': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page_title': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'tld': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['trovetraces']