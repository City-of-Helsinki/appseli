from rest_framework import viewsets
from rest_framework.decorators import api_view, link
from rest_framework.response import Response
from rest_framework.reverse import reverse
from . import models, serializers


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = models.Application.objects.all()
    serializer_class = serializers.ApplicationSerializer


class PlatformViewSet(viewsets.ModelViewSet):
    queryset = models.Platform.objects.all()
    serializer_class = serializers.PlatformSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
