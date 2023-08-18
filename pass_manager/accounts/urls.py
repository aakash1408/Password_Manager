from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("signin/", views.signin),
    path("info/", views.info),
    path("login/", views.login)
]
