from django.http import HttpRequest, HttpResponse
from django.urls import path


def home(request: HttpRequest) -> HttpResponse:
    return HttpResponse("hello world")


urlpatterns = [path("", home)]
