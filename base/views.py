""" Views
"""

from django.shortcuts import render


def home(request):
    """Home page"""
    return render(request, 'home.html')


def room(request, _room_id):
    """Room page"""
    return render(request, 'room.html')
