from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Room(models.Model):
    name = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class Message(models.Model):
    user = models.CharField(max_length=1000000)
    room = models.CharField(max_length=1000000)
    content = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=datetime.now, blank=True)

    
