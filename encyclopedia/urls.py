from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("create_new", views.newpage, name="newpage"),
    path("random_page", views.random, name="random"),
    path("search", views.search, name="search")
]
