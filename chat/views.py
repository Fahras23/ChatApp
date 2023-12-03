from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from .models import Room,Message

def chatPage(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login-user")
    context = {}
    return render(request, "chat/main.html", context) 

# chat/views.py

from django.shortcuts import render
from .models import Room, Message

def room_view(request, room_name):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room_name)
    return render(request, 'chat/room.html', {
        'username': username,
        'room': room_name,
        'room': room_details
    })

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(content=message, user=request.user, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request,room_name):
    messages = Message.objects.all()
    return JsonResponse({"messages":list(messages.values())})