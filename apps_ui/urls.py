from django.conf.urls import patterns, url
from django.views.generic import TemplateView


view = TemplateView.as_view(template_name="apps_ui/index.html")

urlpatterns = patterns('',
    # Catch all and pass to angular. Has to explicitly end in a slash so that
    # APPEND_SLASH is not broken
    url(r'^(.*/)?$', view, name="ui-index"),
)
