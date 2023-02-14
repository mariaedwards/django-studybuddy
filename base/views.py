""" Views
"""

from django.http import HttpResponseBadRequest
from django.db.models import Q
from django.shortcuts import render, redirect
from base.models import Room, Topic
from base.forms import RoomForm


def home(request):
    """Home page"""
    if request.method == 'GET':
        q = ''
        if 'q' in request.GET:
            q = request.GET['q']
        rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(
            description__icontains=q) | Q(host__username__icontains=q))
        room_count = rooms.count()
        topics = Topic.objects.all()
        context = {'rooms': rooms, 'topics': topics, "room_count": room_count}
        return render(request, 'base/home.html', context)
    else:
        return HttpResponseBadRequest()


def room(request, room_id):
    """Room page"""
    if request.method == 'GET':
        current_room = Room.objects.get(pk=room_id)
        context = {"room": current_room}
        return render(request, 'base/room.html', context)
    else:
        return HttpResponseBadRequest()


def create_room(request):
    """Create room page"""
    if request.method == 'GET':
        form = RoomForm()
        context = {'form': form}
        return render(request, 'base/room_form.html', context)
    elif request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        return HttpResponseBadRequest()


def edit_room(request, room_id):
    """Edit room page"""
    current_room = Room.objects.get(pk=room_id)
    if request.method == 'GET':
        form = RoomForm(instance=current_room)
        context = {'form': form}
        return render(request, 'base/room_form.html', context)
    elif request.method == 'POST':
        form = RoomForm(request.POST, instance=current_room)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        return HttpResponseBadRequest()


def delete_room(request, room_id):
    """Delete room page"""
    current_room = Room.objects.get(pk=room_id)
    if request.method == 'GET':
        return render(request, 'base/delete.html', {"obj": current_room})

    if request.method == 'POST':
        current_room.delete()
        return redirect('home')
