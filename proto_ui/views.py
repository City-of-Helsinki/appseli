from django.shortcuts import render, get_object_or_404
from apps import models


def index(request):
    applications = models.Application.objects.all()
    return render(request, "proto_ui/index.html", {
        "applications": applications,
    })


def application(request, pk):
    application = get_object_or_404(models.Application, pk=pk)
    return render(request, "proto_ui/application.html", {
        "application": application,
    })
