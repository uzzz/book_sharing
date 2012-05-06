from django.conf.urls import patterns, url
from users.views import ShowDetailView

urlpatterns = patterns('',
    url(r'(?P<pk>\d+)/$', ShowDetailView.as_view(), name='users_show')
)
