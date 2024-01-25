from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
import pyotp

class Profile(models.Model):  
    user = models.OneToOneField(User,on_delete=models.CASCADE)  
    code = models.CharField(max_length=100,blank=False)
    def __str__(self):
        return self.user.username
    def generate_otp_secret(self):
        if not self.code:
            self.code = pyotp.random_base32()
            self.save()

class Room(models.Model):
    name = models.CharField(max_length=100,blank=False)
    users = models.ManyToManyField(User,blank=True)
    def __str__(self):
        return self.name
    
class Message(models.Model):
    user = models.CharField(max_length=1000000)
    room = models.CharField(max_length=1000000)
    content = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=datetime.now, blank=True)


