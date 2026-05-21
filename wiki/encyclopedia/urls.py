from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("newPage/", views.newPage, name="newPage"),
    path("random/", views.randomPage, name="random"),
    path("search/", views.search, name="search"),
    path("delete/<str:title>", views.delete, name="delete"),
    path("edit/<str:title>/", views.editPage, name="editPage"),
    path("wiki/<str:title>/", views.title, name="wikiTitle"),
    path("<str:title>/", views.title, name="title"),
]
