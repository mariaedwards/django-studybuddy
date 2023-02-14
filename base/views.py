""" Views
"""

from django.shortcuts import render, redirect
from base.models import Room
from base.forms import RoomForm


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


def create_room(request):
    """Create room page"""
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)
