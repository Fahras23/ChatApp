from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

from django.db import models

        
class Room(models.Model):
    name = models.CharField(max_length=100,blank=False)
    author = models.CharField(max_length=100,blank=False)
    user = models.CharField(max_length=100,blank=False)
    additional_users = models.ManyToManyField(User,blank=True)
    def __str__(self):
        return self.name
    
class Message(models.Model):
    user = models.CharField(max_length=1000000)
    room = models.CharField(max_length=1000000)
    content = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=datetime.now, blank=True)

    
