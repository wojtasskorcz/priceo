from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
    url(r'^register/$', 'priceo.views.registration.register', name='register'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
)