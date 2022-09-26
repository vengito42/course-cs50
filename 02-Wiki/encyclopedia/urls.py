from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.entry, name="entry"),
    path("createpage/", views.newpage, name="newpage"),
    path("<str:title>/editpage/", views.editpage, name="editpage"),
    path("randompage/", views.randompage, name="randompage"),
    path("search/", views.search, name="search")
]
