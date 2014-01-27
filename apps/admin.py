from django.contrib import admin
from . import models


admin.site.register(models.Platform)
admin.site.register(models.Application)
admin.site.register(models.ApplicationScreenshot)
admin.site.register(models.ApplicationLanguageSupport)
admin.site.register(models.ApplicationPlatformSupport)
