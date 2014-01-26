from django.db import models

class Platform(models.Model):
    type = models.CharField(max_length=50) # web, android, ios, wp
    name = models.CharField(max_length=100) # translatable

class Application(models.Model):
    name = models.CharField(max_length=100) # translatable
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField() # translatable
    image = models.ImageField(upload_to='apps')
    vendor = models.CharField(max_length=100) # should be ForeignKey?
    rating = models.FloatField() # should be calculated automatically?

class ApplicationScreenshot(models.Model):
    application = models.ForeignKey(Application)
    platform = models.ForeignKey(Platform, null=True)
    image = models.ImageField()
    index = models.PositiveSmallIntegerField()
    image = models.ImageField(upload_to='apps/screenshots')

    class Meta:
        unique_together = (('application', 'platform', 'index'),)

class ApplicationLanguageSupport(models.Model):
    language = models.CharField(max_length=5, db_index=True)
    application = models.ForeignKey(Application, db_index=True)

    class Meta:
        unique_together = (('language', 'application'),)

class ApplicationPlatformSupport(models.Model):
    platform = models.ForeignKey(Platform, db_index=True)
    application = models.ForeignKey(Application, db_index=True)
    platform_link = models.CharField(max_length=200)
    rating = models.FloatField()
    nr_reviews = models.PositiveIntegerField()
    last_updated = models.DateTimeField()

    class Meta:
        unique_together = (('platform', 'platform_link'), ('platform', 'application'))

