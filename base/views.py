""" Views
"""

from django.shortcuts import render
from base.models import Room


def home(request):
    """Home page"""
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request, 'base/home.html', context)


def room(request, room_id):
    """Room page"""
    current_room = Room.objects.get(pk=room_id)
    context = {"room": current_room}
    return render(request, 'base/room.html', context)
