from django.urls import path
from . import views

urlpatterns = [
    path("", views.aviator_game, name="aviator_game"),  # <-- main page
    path("api/bet/", views.bet, name="bet"),
    path("api/cashout/", views.cashout, name="cashout"),
    path("api/plane_crash/", views.plane_crash, name="plane_crash"),
    path("api/new_game/", views.new_game, name="new_game"),
    path("api/start_game/", views.start_game, name="start_game"),
]