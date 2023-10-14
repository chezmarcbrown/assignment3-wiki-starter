from django.urls import path

from . import views

urlpatterns = [
    # test 
    path("", views.index, name="index"),
    path("search/", views.search, name="search"),
    path("edit/<str:title>/", views.edit, name="edit"),
    #path("save/<str:title>/", views.save, name="save"),
    path("random/", views.random, name="random"),
    path("create/", views.create, name="create"),
    path("wiki/<str:title>/", views.entry, name="entry")
]