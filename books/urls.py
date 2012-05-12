from django.conf.urls import patterns, url

from views import *

urlpatterns = patterns('',
    url(r'all/$', AllBooksListView.as_view(), name='all_books'),
    url(r'import/$', import_books, name='import_books'),
    url(r'my/$', MyBooksListView.as_view(), name='my_books'),
    url(r'(?P<pk>\d+)/edit/$', MyBookUpdateView.as_view(),
        name='edit_book'),
    url(r'(?P<pk>\d+)/delete/$', MyBookDeleteView.as_view(),
        name='delete_my_book')
)
