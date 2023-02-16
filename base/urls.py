"""Base App URL Configuration
"""
from django.urls import path
from base import views

urlpatterns = [
    path("login/", views.auth_user, name="auth"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register_user, name="register"),
    path("", views.home, name="home"),
    path("rooms/<int:room_id>/", views.room, name="rooms"),
    path("users/<int:user_id>/", views.users, name="users"),
    path("create-room/", views.create_room, name="create_room"),
    path("edit-room/<int:room_id>/", views.edit_room, name="edit_room"),
    path("delete-room/<int:room_id>/", views.delete_room, name="delete_room"),
    path("delete-message/<int:message_id>/",
         views.delete_message, name="delete_message")
]
