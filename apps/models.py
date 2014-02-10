from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Application(models.Model):
    name = models.CharField(max_length=100)  # translatable
    slug = models.SlugField(max_length=100, unique=True)
    categories = models.ManyToManyField('Category',
                                        blank=True,
                                        related_name='applications')
    accessibilities = models.ManyToManyField('Accessibility',
                                             blank=True,
                                             related_name='applications')
    platforms = models.ManyToManyField('Platform',
                                       blank=True,
                                       related_name='applications',
                                       through='ApplicationPlatformSupport')
    short_description = models.TextField(blank=True)  # translatable
    description = models.TextField()  # translatable
    vendor = models.CharField(max_length=100)  # should be ForeignKey?
    publish_date = models.DateTimeField()
    rating = models.FloatField()  # should be calculated automatically?
    publisher_url = models.CharField(max_length=200, blank=True)
    support_url = models.CharField(max_length=200, blank=True)
    contact_email = models.EmailField(max_length=254, blank=True)
    version = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField()

    def _get_upload_path(instance, filename):
        return 'apps/{}/{}'.format(instance.slug, filename)
    image = models.ImageField(upload_to=_get_upload_path)

    def save(self, *args, **kwargs):
        now = timezone.now()
        if not self.id:
            self.created = now
        self.modified = now
        return super(Application, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class BaseTag(models.Model):
    """Base class for tag-like m2m relations from Application"""
    name = models.CharField(max_length=100)  # translatable
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Platform(BaseTag):
    pass


class Category(BaseTag):
    pass


class Accessibility(BaseTag):
    pass


@python_2_unicode_compatible
class ApplicationScreenshot(models.Model):
    application = models.ForeignKey(Application)
    platform = models.ForeignKey(Platform, null=True)
    index = models.PositiveSmallIntegerField()

    def _get_upload_path(instance, filename):
        return 'apps/{}/screenshots/{}'.format(instance.application.slug,
                                               filename)
    image = models.ImageField(upload_to=_get_upload_path)

    class Meta:
        unique_together = (('application', 'platform', 'index'),)
        ordering = ('index',)

    def __str__(self):
        return "{} #{}".format(self.application, self.index)


@python_2_unicode_compatible
class ApplicationLanguageSupport(models.Model):
    language = models.CharField(max_length=5, db_index=True)
    application = models.ForeignKey(Application, db_index=True,
                                    related_name='languages')

    class Meta:
        unique_together = (('language', 'application'),)

    def __str__(self):
        return "{}: {}".format(self.application, self.language)


@python_2_unicode_compatible
class ApplicationPlatformSupport(models.Model):
    platform = models.ForeignKey(Platform, db_index=True)
    application = models.ForeignKey(Application, db_index=True)
    store_url = models.CharField(max_length=200)
    rating = models.FloatField()
    nr_reviews = models.PositiveIntegerField()
    last_updated = models.DateTimeField()

    class Meta:
        unique_together = (('platform', 'store_url'), ('platform', 'application'))

    def __str__(self):
        return "{}: {}".format(self.application, self.platform)
