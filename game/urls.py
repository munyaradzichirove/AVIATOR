from django.urls import path
from . import views

urlpatterns = [
    path("", views.aviator_game, name="aviator_game"),
]