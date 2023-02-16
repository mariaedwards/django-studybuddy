""" Views
"""

from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from base.models import Room, Topic, Message
from django.contrib.auth.forms import UserCreationForm
from base.forms import RoomForm


def auth_user(request):
    """Auth page"""
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, 'base/auth.html', {'page': 'login'})
    elif request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return HttpResponseBadRequest('Invalid username or password')
        except User.DoesNotExist:
            return HttpResponseBadRequest('Invalid username or password')
    else:
        return HttpResponseNotAllowed(['POST', 'GET'])


def logout_user(request):
    """Logout page"""
    logout(request)
    return redirect('home')


def register_user(request):
    """Register page"""
    if request.method == 'GET':
        context = {'form':  UserCreationForm()}
        return render(request, 'base/auth.html', context)
    elif request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user_name = user.username.lower()
            if User.objects.filter(username=user_name).exists():
                return HttpResponseBadRequest('User already exists')
            else:
                user.username = user_name
                user.save()
                login(request, user)
                return redirect('home')
        else:
            return HttpResponseBadRequest('Error in provided data')
    else:
        return HttpResponseNotAllowed(['POST', 'GET'])


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
        comments = Message.objects.filter(Q(room__topic__name__icontains=q))
        context = {'rooms': rooms, 'topics': topics,
                   "room_count": room_count, "comments": comments}
        return render(request, 'base/home.html', context)
    else:
        return HttpResponseNotAllowed(['GET'])


def users(request, user_id):
    """User profile page"""
    current_user = User.objects.get(pk=user_id)
    if request.method == 'GET':
        rooms = current_user.room_set.all()
        comments = current_user.message_set.all()
        topics = Topic.objects.all()
        context = {"user": current_user, "rooms": rooms,
                   "comments": comments, "topics": topics}
        return render(request, 'base/profile.html', context)
    elif request.method == 'POST':
        pass
    else:
        return HttpResponseNotAllowed(['POST', 'GET'])


def room(request, room_id):
    """Room page"""
    current_room = Room.objects.get(pk=room_id)
    if request.method == 'GET':
        comments = current_room.message_set.all()

        participants = current_room.participants.all()
        context = {"room": current_room, "comments": comments,
                   "participants": participants}
        return render(request, 'base/room.html', context)
    if request.method == 'POST':
        comment = Message.objects.create(
            user=request.user, room=current_room, body=request.POST.get('comment'))
        comment.save()
        current_room.participants.add(request.user)
        return redirect('rooms', room_id=current_room.id)
    else:
        return HttpResponseNotAllowed(['GET'])


@login_required(login_url='auth')
def create_room(request):
    """Create room page"""
    if request.method == 'GET':
        form = RoomForm()
        context = {'form': form}
        return render(request, 'base/room_form.html', context)
    elif request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            new_room = form.save(commit=False)
            new_room.host = request.user
            new_room.save()
            return redirect('home')
    else:
        return HttpResponseNotAllowed(['POST', 'GET'])


@login_required(login_url='auth')
def edit_room(request, room_id):
    """Edit room page"""
    current_room = Room.objects.get(pk=room_id)
    if request.user != current_room.host:
        return HttpResponseForbidden()
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
        return HttpResponseNotAllowed(['POST', 'GET'])


@login_required(login_url='auth')
def delete_room(request, room_id):
    """Delete room page"""
    current_room = Room.objects.get(pk=room_id)
    if request.user != current_room.host:
        return HttpResponseForbidden()
    if request.method == 'GET':
        return render(request, 'base/delete.html', {"obj": current_room})
    elif request.method == 'POST':
        current_room.delete()
        return redirect('home')
    else:
        return HttpResponseNotAllowed(['POST', 'GET'])


@login_required(login_url='auth')
def delete_message(request, message_id):
    """Delete message page"""
    current_message = Message.objects.get(pk=message_id)
    if request.user != current_message.user:
        return HttpResponseForbidden()
    if request.method == 'GET':
        return render(request, 'base/delete.html', {"obj": current_message})
    elif request.method == 'POST':
        current_message.delete()
        return redirect('rooms', room_id=current_message.room.id)
    else:
        return HttpResponseNotAllowed(['POST', 'GET'])
