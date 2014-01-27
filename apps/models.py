from __future__ import unicode_literals
from django.db import models


class Platform(models.Model):
    type = models.CharField(max_length=50)  # web, android, ios, wp
    name = models.CharField(max_length=100)  # translatable

    def __unicode__(self):
        return self.name


class Application(models.Model):
    name = models.CharField(max_length=100)  # translatable
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()  # translatable
    image = models.ImageField(upload_to='apps/icons')
    vendor = models.CharField(max_length=100)  # should be ForeignKey?
    rating = models.FloatField()  # should be calculated automatically?

    def __unicode__(self):
        return self.name


class ApplicationScreenshot(models.Model):
    application = models.ForeignKey(Application)
    platform = models.ForeignKey(Platform, null=True)
    index = models.PositiveSmallIntegerField()
    image = models.ImageField(upload_to='apps/screenshots')

    class Meta:
        unique_together = (('application', 'platform', 'index'),)
        ordering = ('index',)

    def __unicode__(self):
        return "{} #{}".format(self.application, self.index)


class ApplicationLanguageSupport(models.Model):
    language = models.CharField(max_length=5, db_index=True)
    application = models.ForeignKey(Application, db_index=True)

    class Meta:
        unique_together = (('language', 'application'),)

    def __unicode__(self):
        return "{}: {}".format(self.application, self.language)


class ApplicationPlatformSupport(models.Model):
    platform = models.ForeignKey(Platform, db_index=True)
    application = models.ForeignKey(Application, db_index=True)
    platform_link = models.CharField(max_length=200)
    rating = models.FloatField()
    nr_reviews = models.PositiveIntegerField()
    last_updated = models.DateTimeField()

    class Meta:
        unique_together = (('platform', 'platform_link'), ('platform', 'application'))

    def __unicode__(self):
        return "{}: {}".format(self.application, self.platform)
