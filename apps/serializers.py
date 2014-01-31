from rest_framework import serializers
from .models import (
    Application,
    ApplicationPlatformSupport,
    Platform,
)


class SupportedPlatformSerializer(serializers.ModelSerializer):
    name = serializers.Field(source='platform.name')
    type = serializers.Field(source='platform.type')
    url = serializers.HyperlinkedRelatedField(view_name='platform-detail',
                                              source='platform')

    class Meta:
        model = ApplicationPlatformSupport
        fields = ('url', 'name', 'type', 'platform_link',
                  'rating', 'nr_reviews', 'last_updated')


class ApplicationSerializer(serializers.HyperlinkedModelSerializer):
    platforms = SupportedPlatformSerializer(source='applicationplatformsupport_set',
                                            many=True)
    languages = serializers.SlugRelatedField(many=True,
                                             read_only=True,
                                             slug_field='language')

    class Meta:
        model = Application
        fields = ('url', 'name', 'slug', 'description', 'image', 'vendor',
                  'rating', 'publish_date', 'support_link', 'contact_email',
                  'platforms', 'languages')


class PlatformSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Platform
        fields = ('url', 'name', 'type', 'applications')
