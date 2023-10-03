from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("css", views.css, name="CSS"),
    path("django", views.django, name="Django"),
    path("git", views.git, name="Git"),
    path("html", views.html, name="HTML"),
    path("python", views.python, name="Python"),
    path("edit", views.edit, name="Edit")
]
