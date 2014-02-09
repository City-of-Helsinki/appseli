from django.conf.urls import patterns, url, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'application', views.ApplicationViewSet)
router.register(r'platform', views.PlatformViewSet)
router.register(r'category', views.CategoryViewSet)
router.register(r'accessibility', views.AccessibilityViewSet)


urlpatterns =  patterns('',
    url(r'^', include(router.urls)),
    url(r'^auth/', include('rest_framework.urls',
                            namespace='rest_framework')),
)
