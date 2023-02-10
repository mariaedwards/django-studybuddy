"""Models"""

from django.db import models


class Room(models.Model):
    """Room"""
    name = models.CharField(max_length=100)
    # topic = models.CharField(max_length=100)
    # host = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, null=True, blank=True)
    # participants = models.ManyToManyField('User', related_name='participants')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'
