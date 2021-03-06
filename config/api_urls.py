from django.urls import path, include

urlpatterns = [path("tickets/", include("tickets.urls"))]
