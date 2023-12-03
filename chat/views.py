from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from .models import Room,Message

def home(request):
    if not request.user.is_authenticated:
        return redirect("login-user")
    rooms = Room.objects.all()
    context = {'rooms':rooms}
    return render(request,'chat/main.html',context=context)

def room_view(request, room_name):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room_name)
    return render(request, 'chat/room.html', {
        'username': username,
        'room': room_name,
        'room_details': room_details
    })

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']
    new_message = Message.objects.create(content=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request,room_name):
    room = Room.objects.get(name=room_name)
    messages = Message.objects.filter(room=room.id)
    return JsonResponse({"messages":list(messages.values())})

def create_room(request):
    room_name = request.POST['room_name']
    new_room = Room.objects.create(name=room_name)
    new_room.save()
    return HttpResponse()