import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, Message,Registration
from django.contrib.auth.models import User

def get_room_name(sender_id, receiver_id):
    sorted_ids = sorted([sender_id, receiver_id])
    return f"chat_{sorted_ids[0]}_{sorted_ids[1]}"

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.other_user_id = int(self.scope['url_route']['kwargs']['receiver_id'])
        self.room_name = get_room_name(self.user.id, self.other_user_id)
        self.room_group_name = f'chat_{self.room_name}'
        self.room,_ = await database_sync_to_async(Room.objects.get_or_create)(name=self.room_name)
      
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender = self.scope["user"]
        receiver = await database_sync_to_async(User.objects.get)(id=self.other_user_id)
        await database_sync_to_async(Message.objects.create)(
            room=self.room,
            sender=sender,
            receiver=receiver,
            message=message
        )
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender.username,
                'receiver': receiver.username
            }
        )
        
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        receiver = event['receiver']
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'receiver': receiver
        }))
