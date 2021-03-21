
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("video_posts", views.video_posts, name="video_posts"),
    path("video_post/<int:video_id>", views.video_post, name="video_post"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
]
