
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<id>", views.profile, name="profile"),
    path("follow/<id>", views.follow, name='follow'),
    path("unfolow/<id>", views.unfollow, name='unfollow'),
    path("following", views.following, name="following"),
    path("delete/<id>", views.delete, name='delete'),
]
