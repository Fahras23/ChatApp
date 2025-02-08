import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from django.contrib.auth.models import User
from .models import Room, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["id"]
        self.room_group_name = "chat_%s" % self.room_id

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        print(f"WebSocket closed with code {close_code}")
        await self.close()

    async def receive(self, text_data):
        data = json.loads(text_data)

        msg_type = data["type"]
        if msg_type == "chat_message":
            message = data["message"]
            username = data["username"]
            room_id = data["room_id"]

            await self.save_message(username, room_id, message)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "username": username,
                    "room_id": room_id,
                },
            )
        else:
            user = data["user"]
            room_id = data["room_id"]

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_user",
                    "user": user,
                    "room_id": room_id,
                },
            )

    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]
        room_id = event["room_id"]
        msg_type = event["type"]
        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "username": username,
                    "room_id": room_id,
                    "type": msg_type,
                }
            )
        )

    async def chat_user(self, event):
        user = str(event["user"])
        room_id = event["room_id"]
        msg_type = event["type"]

        # check if user exist in db or on room list
        check = await self.check_and_save_user(user, room_id)

        if check == True:
            await self.send(
                text_data=json.dumps(
                    {"user": str(user), "room_id": room_id, "type": msg_type}
                )
            )

    # Decorator for awaiting of processing rest of function till its finished
    @sync_to_async
    def save_message(self, username, room_id, message):
        user = User.objects.get(username=username)
        room = Room.objects.get(id=room_id)

        Message.objects.create(user=user, room=room, content=message)

    @sync_to_async
    def check_and_save_user(self, user, room_id):
        user_obj = User.objects.filter(username=user).first()
        if (
            not user_obj
            or Room.objects.filter(id=room_id, users__username=user).exists()
        ):
            print(f"User '{user}' does not exist. or exist already in chat")
            return False
        room = Room.objects.get(id=room_id)
        add_user = User.objects.filter(username=user).first()
        room.users.add(add_user)
        room.save()
        return True
