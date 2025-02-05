import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from  django.contrib.auth.models import User
from .models import Room, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['id']
        self.room_group_name = 'chat_%s' % self.room_id

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self,close_code):
        await self.channel_layer.group_discard(    
            self.room_group_name,
            self.channel_name
        )

        print(f"WebSocket closed with code {close_code}")
        await self.close()


    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        room_id = data['room_id']
        
        await self.save_message(username, room_id, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'room_id': room_id,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        room_id = event['room_id']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'room_id': room_id,
        }))

    # Decorator for awaiting of processing rest of function till its finished
    @sync_to_async
    def save_message(self, username, room_id, message):
        user = User.objects.get(username=username)
        room = Room.objects.get(id=room_id)

        Message.objects.create(user=user, room=room, content=message)