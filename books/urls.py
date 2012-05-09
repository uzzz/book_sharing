from django.conf.urls import patterns, url
from views import import_books

urlpatterns = patterns('',
    url(r'import/$', import_books, name='import_books')
)
