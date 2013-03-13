from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'(?P<order_by>[-\w]+)/$', 'priceo.views.search.results', 
            name='search_results'),
    url(r'$', 'priceo.views.search.results', 
            {'order_by': '-pub_date'}, name='search_results'),
)