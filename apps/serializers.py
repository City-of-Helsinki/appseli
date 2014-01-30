from rest_framework import serializers
from .models import (
    Application,
    Platform,
)


class ApplicationSerializer(serializers.HyperlinkedModelSerializer):
    # TODO: show the data from ApplicationPlatformSupport
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
