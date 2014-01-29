from django.conf.urls import patterns, include, url
from . import views


urlpatterns = patterns('',
    url(r'^$', views.list_applications, name="proto-applications"),
    url(r'^app/(?P<pk>\d+)/$', views.show_application_details,
        name="proto-application-details"),
)
