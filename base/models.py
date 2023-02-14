"""Models"""

from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):
    """Topic"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'


class Room(models.Model):
    """Room"""
    name = models.CharField(max_length=100)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    # participants = models.ManyToManyField('User', related_name='participants')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return f'{self.name}'


class Message(models.Model):
    """Message"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.CharField(max_length=1000)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{ str(self.body)[:50]}'
