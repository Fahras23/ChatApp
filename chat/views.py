from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Room,Message

#pages
def home(request):
    if not request.user.is_authenticated:
        return redirect("login-user")
    rooms = Room.objects.all()
    print(rooms)
    context = {'rooms':rooms}
    return render(request,'chat/main.html',context=context)

def room_view(request, room_name):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room_name)
    print(room_details)
    if room_details:
        return render(request, 'chat/room.html', {
            'username': username,
            'room': room_name,
            'room_details': room_details
        })
    else:
        return redirect(request.META['HTTP_REFERER'])

def register_user(request):
    return render(request,'chat/register.html')

#functionality
def send(request):
    message = request.POST['message']
    username = request.user
    room_id = request.POST['room_id']
    new_message = Message.objects.create(content=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request,room_name):
    room = Room.objects.get(name=room_name)
    messages = Message.objects.filter(room=room.id)
    return JsonResponse({"messages":list(messages.values())})

def create_room(request):
    #get room_name from view
    room_name = request.POST['room_name']
    rooms = list(Room.objects.values_list('name', flat = True))
    #check if room does exist already
    if room_name in rooms or len(room_name)<3 or len(room_name)>50:
        print('error')
    else:
        new_room = Room.objects.create(name=room_name,user=username)
        new_room.save()
        return redirect(request.META['HTTP_REFERER'])