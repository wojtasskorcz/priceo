from django.conf.urls import patterns, url
from priceo.models import RATING_DOWN, RATING_UP

urlpatterns = patterns('',
    url(r'^(?P<shop_id>\d+)/voteup/$', 'priceo.views.shops.shop_vote', 
        {'rating': RATING_UP}, name='shop_voteup'),
    url(r'^(?P<shop_id>\d+)/votedown/$', 'priceo.views.shops.shop_vote', 
        {'rating': RATING_DOWN}, name='shop_votedown'),
    url(r'^(?P<shop_id>\d+)/$', 'priceo.views.shops.shop_details', name='shop_details'),
)