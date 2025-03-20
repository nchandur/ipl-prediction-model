from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("player", views.player, name="player"),
    path("team", views.team, name="team"),
    path("match", views.match, name="match")
]