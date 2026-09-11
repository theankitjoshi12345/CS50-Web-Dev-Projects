
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.newpost, name="newpost"),
    path("delete/<int:id>", views.delete, name="delete"),
    path("profile/<path:username>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path("follow/<path:username>", views.follow, name="follow"),
    path("unfollow/<path:username>", views.unfollow, name="unfollow"),
    path("edit/<int:id>", views.edit, name="edit"),
    path("likes/<int:id>", views.likes, name="likes"),
]
