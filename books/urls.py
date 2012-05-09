from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from views import *

urlpatterns = patterns('',
    url(r'import/$', import_books, name='import_books'),
    url(r'my/$', login_required(MyBooksListView.as_view()), name='my_books'),
    url(r'(?P<pk>\d+)/delete/$', login_required(MyBookDeleteView.as_view()),
        name='delete_my_book')
)
