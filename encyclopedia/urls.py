from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("create_new", views.newpage, name="newpage"),
    path("search", views.search, name="search"),
    path("rand/", views.rand, name="rand"),
    path("edit/", views.edit, name="edit"),
    path("save_edit/", views.save_edit, name="save_edit")
]
