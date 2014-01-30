from django.conf.urls import patterns, url, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'applications', views.ApplicationViewSet)
router.register(r'platforms', views.PlatformViewSet)


urlpatterns =  patterns('',
    url(r'^', include(router.urls)),
    url(r'^auth/', include('rest_framework.urls',
                            namespace='rest_framework')),
)
