from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/scrape/", views.scrape, name="scrape"),
]
