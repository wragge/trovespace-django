from django.conf.urls import patterns, include, url

from django.contrib import admin
from trovetraces.views import *

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'trovespace.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^traces/$', TracesView.as_view()),
    url(r'^traces/top-pages/$', PageTotalsView.as_view(), name='top-pages'),
    url(r'^traces/top-articles/$', ArticleTotalsView.as_view(), name='top-articles'),
    url(r'^traces/pages/$', PageList.as_view(), name='page-list'),
    url(r'^traces/pages/domain/(?P<domain>[a-z0-9\.]+)/$', PageList.as_view(), name='domain-page-list'),
    url(r'^traces/articles/$', ArticleList.as_view(), name='article-list'),
    url(r'^traces/articles/newspaper/(?P<newspaper>\d+)/$', ArticleList.as_view(), name='newspaper-article-list'),
    url(r'^traces/pages/(?P<pk>\d+)/$', PageView.as_view(), name='page-detail'),
    url(r'^traces/articles/(?P<pk>\d+)/$', ArticleView.as_view(), name='article-detail'),
)
