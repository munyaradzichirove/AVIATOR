from django.urls import path
from . import views

urlpatterns = [
    path("", views.aviator_game, name="aviator_game"), 
    path("api/bet/", views.bet, name="bet"),
    path("api/cashout/", views.cashout, name="cashout"),
    path("api/plane_crash/", views.plane_crash, name="plane_crash"),
    path("api/request_game_id/", views.request_game_id, name="request_game_id"),
    path("api/run_game/", views.run_game, name="run_game"),
]