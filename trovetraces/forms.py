from django import forms
from haystack.forms import SearchForm

class ArticleSearchForm(forms.Form):
	#date = forms.DateField(required=False)
	#order_by = forms.CharField(required=False)
	q = forms.CharField(required=False)


class PageSearchForm(SearchForm):
	#order_by = forms.CharField(required=False)
	
	def no_query_found(self):
		sqs = self.searchqueryset.all().order_by('title')
		return sqs

	def search(self, order_by=None):
		sqs = super(PageSearchForm, self).search()
		if not self.is_valid():
			return self.no_query_found()

		if not self.cleaned_data.get('q'):
		    return self.no_query_found()

		order_by = self.cleaned_data.get('order_by', 'title')
		sqs = sqs.order_by(order_by)

		return sqs