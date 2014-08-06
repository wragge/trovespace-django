# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Page'
        db.create_table(u'trovetraces_page', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file_id', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('page_title', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('domain', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('tld', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('cleaned_html', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'trovetraces', ['Page'])

        # Adding model 'Article'
        db.create_table(u'trovetraces_article', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('page', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('newspaper_id', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('newspaper_title', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal(u'trovetraces', ['Article'])

        # Adding model 'Backlink'
        db.create_table(u'trovetraces_backlink', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('domain', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('href', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('target', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trovetraces.Article'])),
            ('anchor', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('context', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trovetraces.Page'])),
        ))
        db.send_create_signal(u'trovetraces', ['Backlink'])


    def backwards(self, orm):
        # Deleting model 'Page'
        db.delete_table(u'trovetraces_page')

        # Deleting model 'Article'
        db.delete_table(u'trovetraces_article')

        # Deleting model 'Backlink'
        db.delete_table(u'trovetraces_backlink')


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
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trovetraces.Page']"}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['trovetraces.Article']"})
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