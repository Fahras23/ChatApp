from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Room,Message

#pages
def home(request):
    if not request.user.is_authenticated:
        return redirect("login-user")
    if request.method == "POST":
        remove_room = request.POST["room"]
        print(rooms,remove_room)

    rooms = Room.objects.all()
    context = {'rooms':rooms}
    return render(request,'chat/main.html',context=context)

def room_view(request, room_name):
    room_details = Room.objects.get(name=room_name)
    session_user = str(request.user)
    if session_user==room_details.user or session_user==room_details.author or session_user in room_details.additional_users.values_list('username', flat = True):
        return render(request, 'chat/room.html', {
            'username': room_details.user,
            'author': room_details.author,
            'room': room_name,
            'room_details': room_details
        })
    else:
        print("user not authenticated")
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
    username = request.POST['username']
    usernames = username.split(",")
    username = usernames[0]
    additional_users = usernames[1:]
    author = str(request.user)
    users = list(User.objects.values_list('username', flat = True))
    rooms = list(Room.objects.values_list('name', flat = True))
    #check if room does exist already
    if room_name in rooms or len(room_name)<3 or len(room_name)>50:
        print('error')
        return redirect(request.META['HTTP_REFERER'])
    elif all(user in users for user in usernames):
        new_room = Room.objects.create(name=room_name,user=username,author=author)
        if additional_users:
            for add_user in additional_users:
                add_user_obj = User.objects.filter(username=add_user).first()
                new_room.additional_users.add(add_user_obj)
        new_room.save()
        return redirect(request.META['HTTP_REFERER'])
    else:
        print("User does not exist")
        

def remove_room(request,id):
    room = Room.objects.filter(id=id).first()
    if room.author==str(request.user):
        room.delete()
        return redirect(home)
    else:
        return redirect(request.META['HTTP_REFERER'])