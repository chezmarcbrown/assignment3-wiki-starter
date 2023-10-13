from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    # YIKES! This would cause problems when user creates an entry 
    # named edit, save, edd, or rand
    # path("<str:title>", views.entry, name="entry"),
    path("wiki/<str:title>/", views.entry, name="entry"),
    path("edit/<str:title>/", views.edit, name="edit"),
    path("add/", views.add, name="add"),
    path("rand/", views.rand, name="rand")
]
