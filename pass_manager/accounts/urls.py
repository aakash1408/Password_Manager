from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("signin/", views.signin, name = "signin"),
    path("info/", views.info, name = "info"),
    path("login/", views.login_views, name = "login")
]
