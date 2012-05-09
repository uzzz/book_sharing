from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^accounts/', include('registration.urls')),
    (r'^users/', include('users.urls')),
    (r'^$', direct_to_template, { 'template': 'index.html' }, 'index')
)
