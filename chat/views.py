from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.backends import ModelBackend

from io import BytesIO
import pyotp
import qrcode
import io
import base64
from PIL import Image

from .models import Room, Message, Profile
from .forms import UserForm, LoginForm, OTPForm

def home(request):
    if request.user.is_authenticated is False:
        return redirect("login-user")
    if request.method == "POST":
        remove_room = request.POST["room"]
        print(rooms, remove_room)

    rooms = Room.objects.filter(users=request.user)
    print(rooms)
    context = {"rooms": rooms}
    return render(request, "chat/main.html", context=context)


@login_required
def room_view(request, id):
    room_details = Room.objects.get(id=id)
    messages = Message.objects.filter(room=room_details.id)

    if request.method == "POST":
        add_user = request.POST.get("username")
        if add_user in list(User.objects.values_list("username", flat=True)):
            add_user_obj = User.objects.filter(username=add_user).first()
            room_details.users.add(add_user_obj)
            room_details.save()
    session_user = str(request.user)
    usernames = room_details.users.values_list("username", flat=True)
    if session_user in usernames:
        return render(
            request,
            "chat/room.html",
            {
                "usernames": usernames,
                "room": room_details.name,
                "room_details": room_details,
                "messages": messages,
            },
        )
    else:
        print("user not authenticated")

def create_room(request):
    # get room_name from view
    room_name = request.POST["room_name"]
    username = request.POST["username"]
    usernames = list(username.split(","))
    author = str(request.user)
    print(author)
    usernames.append(author)
    print(usernames)
    users = list(User.objects.values_list("username", flat=True))
    rooms = list(Room.objects.values_list("name", flat=True))
    # check if room does exist already
    if room_name in rooms or len(room_name) < 3 or len(room_name) > 50:
        print("error")
        return redirect(request.META["HTTP_REFERER"])
    elif all(user in users for user in usernames):
        new_room = Room.objects.create(name=room_name)
        if usernames:
            for add_user in usernames:
                add_user_obj = User.objects.filter(username=add_user).first()
                new_room.users.add(add_user_obj)
        new_room.save()
        return redirect(request.META["HTTP_REFERER"])
    else:
        print("One of users does not exist")
        return redirect(request.META["HTTP_REFERER"])


def remove_room(request, id):
    room = Room.objects.filter(id=id).first()
    usernames = room.users.values_list("username", flat=True)
    if str(request.user) in usernames:
        room.delete()
        return redirect(home)
    else:
        return redirect(request.META["HTTP_REFERER"])


def register_user(request):

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = Profile(user=user)
            profile.generate_otp_secret()
            profile.save()

            authenticate(username=user.username, password=user.password)
            login(request, user)
            return redirect("auth")
    else:
        user_form = UserForm()

    return render(request, "chat/register.html", {"user_form": user_form})


def login_user(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None and form.is_valid():
                # User is authenticated with username and password
                otp_form = OTPForm(request.POST)
                if otp_form:
                    user_profile = User.objects.get(username=username)
                    code = form.cleaned_data.get("code")
                    if pyotp.TOTP(user_profile.profile.code).verify(code):
                        login(request, user_profile, backend='django.contrib.auth.backends.ModelBackend')
                        return redirect("home") 
                    else:
                        print("wrong otp code")
                        messages.add_message(request, messages.ERROR,"Wrong otp code")
                        redirect("login-user") 
            print("wrong input")
            messages.add_message(request, messages.ERROR,"Wrong input")
            redirect("login-user") 
    else:   
        form = LoginForm()
    return render(request, "chat/login.html", {"form": form})


@login_required
def qr_code(request):
    user_profile = request.user.profile
    otp_url = pyotp.totp.TOTP(user_profile.code).provisioning_uri(
        request.user.email, issuer_name=request.user.username
    )
    qr = qrcode.make(otp_url)
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    return render(request, "chat/auth.html", {"qr_base64": qr_base64})
