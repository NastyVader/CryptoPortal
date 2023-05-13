from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path("", views.intro, name="intro"),
    path("login", views.login, name="login"),
]
