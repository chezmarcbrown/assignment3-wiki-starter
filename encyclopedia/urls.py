from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry_title>", views.entry, name="entry"),
    path("random_page", views.random_page, name="random_page"),
    path("new_page", views.new_page, name="new_page"),
    path("edit_page/<str:entry_title>", views.edit_page, name="edit_page"),
    path("search", views.search, name="search")
]
