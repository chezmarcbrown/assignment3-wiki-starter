from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("css", views.css, name="CSS"),
    path("django", views.css, name="Django"),
    path("git", views.css, name="Git"),
    path("html", views.css, name="HTML"),
    path("python", views.css, name="Python")
]
