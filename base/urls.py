"""Base App URL Configuration
"""
from django.urls import path
from base import views

urlpatterns = [
    path("", views.home, name="home"),
    path("rooms/<int:room_id>/", views.room, name="rooms"),
    path("create-room/", views.create_room, name="create_room")
]
