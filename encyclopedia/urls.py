from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("new_entry/", views.new_entry, name="new-entry"),
    path("random_entry/", views.random_entry, name="random-entry"),
    path("new_entry_form/", views.new_entry_form, name="new-entry-form"),
    path("wiki/<str:title>/edit", views.edit_entry, name="edit-entry")
]
