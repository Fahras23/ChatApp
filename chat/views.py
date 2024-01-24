from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from .models import Room,Message,Profile
from .forms import UserForm,LoginForm
import pyotp
import qrcode
from django.contrib.auth.decorators import login_required
import base64

#pages
@login_required
def home(request):
    if request.method == "POST":
        remove_room = request.POST["room"]
        print(rooms,remove_room)
    
    rooms = Room.objects.filter(users=request.user)
    print(rooms)
    context = {'rooms':rooms}
    return render(request,'chat/main.html',context=context)

@login_required
def room_view(request, id):
    room_details = Room.objects.get(id=id)
    if request.method=="POST":
       add_user = request.POST.get('username')
       if add_user in list(User.objects.values_list('username', flat = True)):
            add_user_obj = User.objects.filter(username=add_user).first()
            room_details.users.add(add_user_obj)
            room_details.save()
    session_user = str(request.user)
    usernames = room_details.users.values_list('username', flat = True)
    if session_user in usernames:
        return render(request, 'chat/room.html', {
            'usernames': usernames,
            'room': room_details.name,
            'room_details': room_details
        })
    else:
        print("user not authenticated")
        return redirect(request.META['HTTP_REFERER'])

def register_user(request):
    key = pyotp.random_base32()
    uri = pyotp.totp.TOTP(key).provisioning_uri(
            name='chatapp', 
            issuer_name="key") 
    qrcode.make(uri).save("static/qr.png")
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)  # Hash password
            user.save()

            profile = Profile()
            profile.user = user
            profile.code = key
            profile.save()
            return redirect('login-user')
    else:
        user_form = UserForm()

    return render(request,'chat/register.html',{'user_form': user_form})


#functionality
def send(request):
    message = request.POST['message']
    room_id = request.POST['room_id']
    username = request.user
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
    usernames = list(username.split(","))
    author = str(request.user)
    usernames.append(author)
    print(usernames)
    users = list(User.objects.values_list('username', flat = True))
    rooms = list(Room.objects.values_list('name', flat = True))
    #check if room does exist already
    if room_name in rooms or len(room_name)<3 or len(room_name)>50:
        print('error')
        return redirect(request.META['HTTP_REFERER'])
    elif all(user in users for user in usernames):
        new_room = Room.objects.create(name=room_name)
        if usernames:
            for add_user in usernames:
                add_user_obj = User.objects.filter(username=add_user).first()
                new_room.users.add(add_user_obj)
        new_room.save()
        return redirect(request.META['HTTP_REFERER'])
    else:
        print("One of users does not exist")
        return redirect(request.META['HTTP_REFERER'])
        

def remove_room(request,id):
    room = Room.objects.filter(id=id).first()
    usernames = room.users.values_list('username', flat = True)
    if str(request.user) in usernames:
        room.delete()
        return redirect(home)
    else:
        return redirect(request.META['HTTP_REFERER'])

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            code = form.cleaned_data.get('code')
            print(code)
            user_hash = User.objects.filter(username=username).first().profile.code
            user_hash = user_hash.encode('utf-8')
            user_hash = base64.b32encode(user_hash)
            totp = pyotp.TOTP(user_hash)
            verify = totp.verify(code)
            print(verify)
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'chat/login.html', {'form': form})