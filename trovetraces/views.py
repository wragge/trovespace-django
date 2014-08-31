from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Count
from django.template import RequestContext
from django.views.generic.edit import FormMixin
from haystack.views import SearchView
from haystack.query import SearchQuerySet
from trovetraces.models import Backlink, Page, Article
from trovetraces.forms import ArticleSearchForm, PageSearchForm

# Create your views here.

class TracesView(TemplateView):
	template_name = 'trovetraces/home.html'

	def get_context_data(self, **kwargs):
		context = super(TracesView, self).get_context_data(**kwargs)
		context['backlinks'] = Backlink.objects.all().count()
		context['pages'] = Page.objects.exclude(backlink__isnull=True).count()
		context['articles'] = Article.objects.all().count()
		context['domains'] = Page.objects.exclude(backlink__isnull=True).values('domain').distinct().count()
		return context


class BacklinkList(ListView):
	model = Backlink
	paginate_by = 25


class ListSearchView(ListView, FormMixin):
	order_by = None
	searchqueryset = SearchQuerySet().filter(has_links=True)

	def get_queryset(self):
		"""Return filtered queryset. Uses form_valid() or form_invalid()."""
		form = self.form_class(self.request.GET)
		if form.is_valid() :
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def form_valid(self, form):
		q = form.cleaned_data.get('q', '')
		order_by = self.request.GET.get('order_by', self.order_by)
		sqs = self.searchqueryset
		if q:
			sqs = sqs.auto_query(q)
		sqs = sqs.order_by(order_by)
		return sqs

	def form_invalid(self, form):
		print 'invalid'
		return self.form_empty()

	def form_empty(self):
		order_by = self.request.GET.get('order_by', self.order_by)
		sqs = self.searchqueryset
		sqs = sqs.order_by(order_by)
		return sqs

class PageSearchView(ListSearchView):
	template_name = 'trovetraces/page_list.html'
	paginate_by = 25
	form_class = PageSearchForm
	searchqueryset = SearchQuerySet().models(Page).filter(has_links=True)
	order_by = 'title'

	def form_valid(self, form):
		q = form.cleaned_data.get('q', '')
		self.query = q
		domain = self.kwargs.get('domain')
		self.domain = domain
		order_by = self.request.GET.get('order_by')
		sqs = self.searchqueryset
		if q:
			sqs = sqs.auto_query(q)
		elif not order_by:
			order_by = self.order_by
		if domain:
			sqs = sqs.filter(domain=domain)
		if order_by:
			sqs = sqs.order_by(order_by)
			self.current_order = order_by
		return sqs

	def get_context_data(self, **kwargs):
		kwargs = ListView.get_context_data(self, **kwargs)
		kwargs['query'] = self.query
		if self.domain:
			kwargs['domain'] = self.domain
		kwargs['order'] = self.current_order
		return kwargs


class ArticleSearchView(ListSearchView):
	template_name = 'trovetraces/article_list.html'
	paginate_by = 25
	form_class = ArticleSearchForm
	searchqueryset = SearchQuerySet().models(Article).filter(has_links=True)
	order_by = 'date'
	current_order = None

	def form_valid(self, form):
		q = form.cleaned_data.get('q', '')
		self.query = q
		newspaper_id = self.kwargs.get('newspaper')
		self.newspaper_id = newspaper_id
		order_by = self.request.GET.get('order_by')
		sqs = self.searchqueryset
		if q:
			sqs = sqs.auto_query(q)
		elif not order_by:
			order_by = self.order_by
		if newspaper_id:
			sqs = sqs.filter(newspaper_id=newspaper_id)
		if order_by:
			sqs = sqs.order_by(order_by)
			self.current_order = order_by
		return sqs

	def get_context_data(self, **kwargs):
		kwargs = ListView.get_context_data(self, **kwargs)
		kwargs['query'] = self.query
		if self.newspaper_id:
			kwargs['newspaper'] = Article.objects.values('newspaper_title', 'newspaper_id').filter(newspaper_id=self.newspaper_id)[0]
		kwargs['order'] = self.current_order
		return kwargs


class PageList(ListView):
	model = Page
	queryset = Page.objects.exclude(backlink__isnull=True).order_by('page_title')
	paginate_by = 25

	def get_queryset(self):
		queryset = Page.objects.exclude(backlink__isnull=True)
		domain = self.kwargs.get('domain')
		if domain:
			queryset = queryset.filter(domain=self.kwargs['domain'])
		self.domain = domain
		queryset = queryset.order_by('page_title')
		return queryset

	def get_context_data(self, **kwargs):
	    # Call the base implementation first to get a context
	    context = super(PageList, self).get_context_data(**kwargs)
	    if self.domain:
	    	context['domain'] = self.domain
	    return context


class ArticleList(ListView):
	model = Article
	queryset = Article.objects.exclude(backlink__isnull=True).order_by('date')
	paginate_by = 25

	def get_queryset(self):
		queryset = Article.objects.exclude(backlink__isnull=True)
		newspaper_id = self.kwargs.get('newspaper')
		if newspaper_id:
			queryset = queryset.filter(newspaper_id=newspaper_id)
		self.newspaper_id = newspaper_id
		queryset = queryset.order_by('date')
		return queryset

	def get_context_data(self, **kwargs):
	    # Call the base implementation first to get a context
	    context = super(ArticleList, self).get_context_data(**kwargs)
	    if self.newspaper_id:
	    	context['newspaper'] = Article.objects.values('newspaper_title', 'newspaper_id').filter(newspaper_id=self.newspaper_id)[0]
	    return context


class PageView(DetailView):
	model = Page

	def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
		context = super(PageView, self).get_context_data(**kwargs)
		articles = []
		backlinks = Backlink.objects.filter(page=self.object)
		for link in backlinks:
			if link.target not in articles:
				articles.append(link.target)
		context['articles'] = articles
		return context


class ArticleView(DetailView):
	model = Article

	def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
		context = super(ArticleView, self).get_context_data(**kwargs)
		pages = []
		backlinks = Backlink.objects.filter(target=self.object)
		for link in backlinks:
			if link.page not in pages:
				pages.append(link.page)
		context['pages'] = pages
		return context


class PageTotalsView(TemplateView):
	template_name = 'trovetraces/page-totals.html'

	def get_context_data(self, **kwargs):
		context = super(PageTotalsView, self).get_context_data(**kwargs)
		context['top_pages'] = Page.objects.exclude(backlink__isnull=True).annotate(total_links=Count('backlink')).order_by('-total_links')[:10]
		context['top_domains'] = Page.objects.exclude(backlink__isnull=True).values('domain').annotate(total_links=Count('backlink')).order_by('-total_links')[:10]
		context['top_domain_pages'] = Page.objects.exclude(backlink__isnull=True).values('domain').annotate(total_pages=Count('url')).order_by('-total_pages')[:10]
		return context


class ArticleTotalsView(TemplateView):
	template_name = 'trovetraces/article-totals.html'

	def get_context_data(self, **kwargs):
		context = super(ArticleTotalsView, self).get_context_data(**kwargs)
		context['top_articles'] = Article.objects.annotate(total_links=Count('backlink')).order_by('-total_links')[:10]
		context['top_newspapers'] = Article.objects.values('newspaper_title', 'newspaper_id').annotate(total_links=Count('backlink')).order_by('-total_links')[:10]
		context['top_newspaper_articles'] = Article.objects.values('newspaper_title', 'newspaper_id').annotate(total_articles=Count('url')).order_by('-total_articles')[:10]
		return context