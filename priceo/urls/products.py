from django.conf.urls import patterns, include, url
from priceo.models import RATING_DOWN, RATING_UP

urlpatterns = patterns('',
    url(r'^(?P<product_id>\d+)/voteup/$', 'priceo.views.products.product_vote', 
        {'rating': RATING_UP}, name='product_voteup'),
    url(r'^(?P<product_id>\d+)/votedown/$', 'priceo.views.products.product_vote', 
        {'rating': RATING_DOWN}, name='product_votedown'),
    url(r'^(?P<product_id>\d+)/$', 'priceo.views.products.product_details', name='product_details'),
)