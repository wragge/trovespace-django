import re
from unidecode import unidecode
from haystack import indexes
from trovetraces.models import Page, Article


class PageIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True, use_template=True)
	title = indexes.CharField(model_attr='page_title')
	title_search = indexes.CharField(model_attr='page_title')
	domain = indexes.CharField(model_attr='domain', faceted=True)
	tld = indexes.CharField(model_attr='tld', faceted=True)
	has_links = indexes.BooleanField()
	links = indexes.IntegerField()

	def get_model(self):
		return Page

	def prepare_has_links(self, obj):
		return True if obj.backlink_set.count() > 0 else False

	def prepare_title(self, obj):
		return format_text_for_sort( obj.page_title, remove_articles=True )

	def prepare_links(self, obj):
		return obj.backlink_set.count()


class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True, use_template=True)
	title = indexes.CharField(model_attr='title')
	title_search = indexes.CharField(model_attr='title')
	newspaper_id = indexes.CharField(model_attr='newspaper_id', faceted=True)
	newspaper_title = indexes.CharField(model_attr='newspaper_title')
	date = indexes.DateField(model_attr='date')
	year = indexes.IntegerField(faceted=True)
	has_links = indexes.BooleanField()
	links = indexes.IntegerField()

	def get_model(self):
		return Article

	def prepare_has_links(self, obj):
		return True if obj.backlink_set.count() > 0 else False

	def prepare_year(self, obj):
		return obj.date.year

	def prepare_title(self, obj):
		return format_text_for_sort( obj.title, remove_articles=True )

	def prepare_links(self, obj):
		return obj.backlink_set.count()


def format_text_for_sort(sort_term,remove_articles=False):
    ''' processes text for sorting field:
        * converts non-ASCII characters to ASCII equivalents
        * converts to lowercase
        * (optional) remove leading a/the
        * removes outside spaces
    '''
    sort_term = unidecode(sort_term).lower().strip()
    if remove_articles:
    	sort_term =  re.sub(r'^(a\s+|the\s+)', '', sort_term )
	return sort_term
