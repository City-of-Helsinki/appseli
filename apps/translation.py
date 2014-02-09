from modeltranslation.translator import translator, TranslationOptions
from apps.models import *


class ApplicationTranslationOptions(TranslationOptions):
    fields = ('name', 'description')
translator.register(Application, ApplicationTranslationOptions)


class BaseTagTranslationOptions(TranslationOptions):
    fields = ('name',)
translator.register(Platform, BaseTagTranslationOptions)
translator.register(Category, BaseTagTranslationOptions)
translator.register(Accessibility, BaseTagTranslationOptions)
