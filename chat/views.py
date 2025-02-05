from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from .models import Room,Message,Profile
from .forms import UserForm,LoginForm,OTPForm
import pyotp
import qrcode
from django.contrib.auth.decorators import login_required
import base64

def home(request):
    if request.user.is_authenticated is False:
        return redirect('login-user')
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
    messages = Message.objects.filter(room=room_details.id)

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
            'room_details': room_details,
            'messages': messages
        })
    else:
        print("user not authenticated")

#functionality
def send(request):
    message = request.POST['message']
    room_id = request.POST['room_id']
    username = str(request.user)
    if message:
        new_message = Message.objects.create(content=message, user=username, room_id=room_id)
        new_message.save()
        print('Message sent successfully')
    else:
        print('Message inncorrect')
    
def getMessages(request,room_name):
    room = Room.objects.get(name=room_name)
    messages = Message.objects.filter(room=room)
    return JsonResponse({"messages":list(messages.values())})

def create_room(request):
    #get room_name from view
    room_name = request.POST['room_name']
    username = request.POST['username']
    usernames = list(username.split(","))
    author = str(request.user)
    print(author)
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

def register_user(request):

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = Profile(user=user)
            profile.generate_otp_secret()
            profile.save()

            authenticate(username=user.username,password=user.password)
            login(request,user)
            return redirect('auth')
    else:
        user_form = UserForm()

    return render(request,'chat/register.html',{'user_form': user_form})

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            if username is not None and form.is_valid():
                # User is authenticated with username and password
                otp_form = OTPForm(request.POST)
                if otp_form:
                    user_profile = User.objects.get(username=username)
                    code = form.cleaned_data.get('code')
                    if pyotp.TOTP(user_profile.profile.code).verify(code):
                        login(request, user_profile)
                        return redirect('home')
                    else:
                        # OTP verification failed
                        pass
    else:
        form = LoginForm()
    return render(request, 'chat/login.html', {'form': form})

@login_required
def qr_code(request):
    user_profile = request.user.profile
    otp_url = pyotp.totp.TOTP(user_profile.code).provisioning_uri(request.user.email, issuer_name=request.user.username)
    qrcode.make(otp_url).save("static/qr.png") 
    
    return render(request,'chat/auth.html')
