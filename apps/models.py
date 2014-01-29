from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Platform(models.Model):
    type = models.CharField(max_length=50)  # web, android, ios, wp
    name = models.CharField(max_length=100)  # translatable

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Application(models.Model):
    name = models.CharField(max_length=100)  # translatable
    slug = models.SlugField(max_length=100, unique=True)
    category = models.ForeignKey('Category',
                                 related_name='applications',
                                 null=True)
    platforms = models.ManyToManyField('Platform',
                                       related_name='applications',
                                       through='ApplicationPlatformSupport')
    description = models.TextField()  # translatable
    image = models.ImageField(upload_to='apps/icons')
    vendor = models.CharField(max_length=100)  # should be ForeignKey?
    publish_date = models.DateTimeField()
    rating = models.FloatField()  # should be calculated automatically?
    support_link = models.CharField(max_length=200, blank=True)
    contact_email = models.EmailField(max_length=254, blank=True)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField(max_length=100)  # translatable
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class ApplicationScreenshot(models.Model):
    application = models.ForeignKey(Application)
    platform = models.ForeignKey(Platform, null=True)
    index = models.PositiveSmallIntegerField()
    image = models.ImageField(upload_to='apps/screenshots')

    class Meta:
        unique_together = (('application', 'platform', 'index'),)
        ordering = ('index',)

    def __str__(self):
        return "{} #{}".format(self.application, self.index)


@python_2_unicode_compatible
class ApplicationLanguageSupport(models.Model):
    language = models.CharField(max_length=5, db_index=True)
    application = models.ForeignKey(Application, db_index=True)

    class Meta:
        unique_together = (('language', 'application'),)

    def __str__(self):
        return "{}: {}".format(self.application, self.language)


@python_2_unicode_compatible
class ApplicationPlatformSupport(models.Model):
    platform = models.ForeignKey(Platform, db_index=True)
    application = models.ForeignKey(Application, db_index=True)
    platform_link = models.CharField(max_length=200)
    rating = models.FloatField()
    nr_reviews = models.PositiveIntegerField()
    last_updated = models.DateTimeField()

    class Meta:
        unique_together = (('platform', 'platform_link'), ('platform', 'application'))

    def __str__(self):
        return "{}: {}".format(self.application, self.platform)
