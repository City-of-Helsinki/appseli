import django_filters
from rest_framework import filters, viewsets
from rest_framework.decorators import api_view, link
from rest_framework.response import Response
from rest_framework.reverse import reverse
from . import models, serializers


class ApplicationFilterSet(django_filters.FilterSet):
    category = django_filters.CharFilter(name="category__slug")
    min_rating = django_filters.NumberFilter(name="rating", lookup_type="gte")
    max_Rating = django_filters.NumberFilter(name="rating", lookup_type="lte")

    class Meta:
        model = models.Application
        # TODO: filter by different language names
        fields = ["name", "category", "description", "vendor"]


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = models.Application.objects.all()
    serializer_class = serializers.ApplicationSerializer
    filter_class = ApplicationFilterSet
    filter_backends = (filters.DjangoFilterBackend,
                       filters.SearchFilter,
                       filters.OrderingFilter,)
    search_fields = ("name_fi", "name_en", "name_sv", "name_ru",
                     "description_fi", "description_en",
                     "description_sv", "description_ru",
                     "vendor")
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
