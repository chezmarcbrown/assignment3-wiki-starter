from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("<str:title>", views.entry, name="entry"),
    path("edit/", views.edit, name="edit"),
    path("save/", views.save, name="save"),
    path("add/", views.add, name="add"),
    path("rand/", views.rand, name="rand")
]
