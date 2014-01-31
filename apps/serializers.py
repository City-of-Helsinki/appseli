from rest_framework import serializers
from . import models


class SupportedPlatformSerializer(serializers.ModelSerializer):
    name = serializers.Field(source='platform.name')
    type = serializers.Field(source='platform.type')
    url = serializers.HyperlinkedRelatedField(view_name='platform-detail',
                                              source='platform')

    class Meta:
        model = models.ApplicationPlatformSupport
        fields = ('url', 'name', 'type', 'platform_link',
                  'rating', 'nr_reviews', 'last_updated')


class ApplicationSerializer(serializers.HyperlinkedModelSerializer):
    platforms = SupportedPlatformSerializer(source='applicationplatformsupport_set',
                                            read_only=True,
                                            many=True)
    languages = serializers.SlugRelatedField(many=True,
                                             read_only=True,
                                             slug_field='language')
    image = serializers.SerializerMethodField('get_full_image_url')

    class Meta:
        model = models.Application
        fields = ('url', 'name', 'slug', 'description', 'category', 'image',
                  'vendor', 'rating', 'publish_date', 'support_link',
                  'contact_email', 'platforms', 'languages')

    def get_full_image_url(self, obj):
        request = self.context["request"]
        return request.build_absolute_uri(obj.image.url)


class PlatformSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Platform
        fields = ('url', 'name', 'type', 'applications')


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Category
        fields = ('url', 'name', 'slug', 'applications')
