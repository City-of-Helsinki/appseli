from modeltranslation.translator import translator, TranslationOptions
from apps.models import *


class PlatformTranslationOptions(TranslationOptions):
    fields = ('name',)
translator.register(Platform, PlatformTranslationOptions)


class ApplicationTranslationOptions(TranslationOptions):
    fields = ('name', 'description')
translator.register(Application, ApplicationTranslationOptions)


class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)
translator.register(Category, CategoryTranslationOptions)
