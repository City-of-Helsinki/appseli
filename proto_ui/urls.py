from django.conf.urls import patterns, include, url
from . import views


urlpatterns = patterns('',
    url(r'^$', views.index, name="proto-index"),
    url(r'^app/(?P<pk>\d+)/$', views.application, name="proto-application"),
)
