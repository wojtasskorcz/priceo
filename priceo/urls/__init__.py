from django.conf.urls import patterns, include, url
from django.contrib import admin
from priceo import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                 {'document_root': settings.MEDIA_ROOT}),
#    url(r'^$', 'priceo.views.home', name='home'),
    url(r'^products/', include('priceo.urls.products')),
    url(r'^shops/', include('priceo.urls.shops')),
    url(r'^registration/', include('priceo.urls.registration')),
    url(r'^categories/', include('priceo.urls.categories')),
#    (r'^comments/', include('django.contrib.comments.urls')),
    url(r'^search/', include('priceo.urls.search')),
    url(r'^$', 'priceo.views.home', name='home'),
)
