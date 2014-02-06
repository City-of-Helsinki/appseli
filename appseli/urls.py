from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import RedirectView


ANGULAR_PROTO_INDEX_URL = "{}angular_proto/index.html".format(settings.STATIC_URL)


admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^proto/', include("proto_ui.urls")),
    url(r'^angular/$', RedirectView.as_view(url=ANGULAR_PROTO_INDEX_URL)),
    url(r'^v1/', include("apps.urls")),
)

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

urlpatterns += patterns('',
    url(r'^', include("apps_ui.urls")),
)
