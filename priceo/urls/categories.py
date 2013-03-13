from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^(?P<category_id>\d+)/(?P<order_by>[-\w]+)/$', 'priceo.views.categories.category_details',
            name='category_details'),
#    url(r'^(?P<category_id>\d+)/$', 'priceo.views.categories.category_details', name='category_details'),
    url(r'^(?P<category_id>\d+)/$', 'priceo.views.categories.category_details', 
            {'order_by': '-pub_date'}, name='category_details'),
)