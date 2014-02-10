from __future__ import unicode_literals
from django.conf import settings
from rest_framework import serializers
from . import models


class TranslatedField(serializers.Field):
    def field_to_native(self, obj, field_name):
        # If source is given, use it as the attribute(chain) of obj to be
        # translated and ignore the original field_name
        if self.source:
            bits = self.source.split(".")
            field_name = bits[-1]
            for name in bits[:-1]:
                obj = getattr(obj, name)

        return {
            code: getattr(obj, field_name + "_" + code, None)
            for code, _ in settings.LANGUAGES
        }


def get_full_image_url(self, obj):
    request = self.context["request"]
    return request.build_absolute_uri(obj.image.url)


def create_tag_serializer(model_class):
    class TagSerializer(serializers.HyperlinkedModelSerializer):
        name = TranslatedField()

        class Meta:
            model = model_class
            fields = ('url', 'id', 'name', 'slug', 'applications')
    return TagSerializer


CategorySerializer = create_tag_serializer(models.Category)
PlatformSerializer = create_tag_serializer(models.Platform)
AccessibilitySerializer = create_tag_serializer(models.Accessibility)


class SupportedPlatformSerializer(serializers.ModelSerializer):
    """
    PlatformSerializer with custom fields from ApplicationPlatformSupport
    """
    name = TranslatedField(source="platform.name")
    slug = serializers.Field(source='platform.slug')
    url = serializers.HyperlinkedRelatedField(view_name='platform-detail',
                                              source='platform')

    class Meta:
        model = models.ApplicationPlatformSupport
        fields = ('url', 'id', 'name', 'slug', 'store_url',
                  'rating', 'nr_reviews', 'last_updated')


class SupportedCategorySerializer(CategorySerializer):
    class Meta(CategorySerializer.Meta):
        fields = ('url', 'id', 'name', 'slug')


class SupportedAccessibilitySerializer(AccessibilitySerializer):
    class Meta(CategorySerializer.Meta):
        fields = ('url', 'id', 'name', 'slug')


class ScreenshotSerializer(serializers.ModelSerializer):
    platform = serializers.Field(source='platform.slug')
    image = serializers.SerializerMethodField('get_full_image_url')

    class Meta:
        model = models.ApplicationScreenshot
        fields = ('image', 'platform')

    get_full_image_url = get_full_image_url


class ApplicationSerializer(serializers.HyperlinkedModelSerializer):
    name = TranslatedField()
    short_description = TranslatedField()
    description = TranslatedField()
    platforms = SupportedPlatformSerializer(source='applicationplatformsupport_set',
                                            read_only=True,
                                            many=True)
    languages = serializers.SlugRelatedField(many=True,
                                             read_only=True,
                                             slug_field='language')
    image = serializers.SerializerMethodField('get_full_image_url')
    categories = SupportedCategorySerializer(read_only=True)
    accessibilities = SupportedAccessibilitySerializer(read_only=True)
    screenshots = ScreenshotSerializer(source="applicationscreenshot_set",
                                       many=True,
                                       read_only=True)

    class Meta:
        model = models.Application
        fields = ('url', 'id', 'name', 'slug', 'image', 'short_description',
                  'description', 'vendor', 'publish_date', 'rating',
                  'publisher_url', 'support_url', 'contact_email', 'created',
                  'modified', 'languages', 'categories', 'accessibilities',
                  'platforms','screenshots')

    get_full_image_url = get_full_image_url
