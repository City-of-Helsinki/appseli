import django_filters
from rest_framework import filters, viewsets
from rest_framework.decorators import api_view, link
from rest_framework.response import Response
from rest_framework.reverse import reverse
from . import models, serializers


APPLICATION_SEARCH_FIELDS = (
    "name_fi", "name_en", "name_sv", "name_ru",
    "description_fi", "description_en", "description_sv", "description_ru",
    "vendor",
)


class ApplicationFilterSet(django_filters.FilterSet):
    category = django_filters.CharFilter(name="categories__slug")
    accessibility = django_filters.CharFilter(name="accessibilities__slug")
    platform = django_filters.CharFilter(name="platforms__slug")
    language = django_filters.CharFilter(name="languages__language")
    min_rating = django_filters.NumberFilter(name="rating", lookup_type="gte")
    max_rating = django_filters.NumberFilter(name="rating", lookup_type="lte")

    class Meta:
        model = models.Application
        fields = APPLICATION_SEARCH_FIELDS + ("category", "accessibility",
                 "platform", "min_rating", "max_rating")


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = models.Application.objects.all()
    serializer_class = serializers.ApplicationSerializer
    filter_class = ApplicationFilterSet
    filter_backends = (filters.DjangoFilterBackend,
                       filters.SearchFilter,
                       filters.OrderingFilter,)
    search_fields = APPLICATION_SEARCH_FIELDS
    ordering_fields = ("publish_date", "created", "modified")
    ordering = ("created",)


class PlatformViewSet(viewsets.ModelViewSet):
    queryset = models.Platform.objects.all()
    serializer_class = serializers.PlatformSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer


class AccessibilityViewSet(viewsets.ModelViewSet):
    queryset = models.Accessibility.objects.all()
    serializer_class = serializers.AccessibilitySerializer
