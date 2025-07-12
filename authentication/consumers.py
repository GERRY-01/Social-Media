import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, Message,Registration
from django.contrib.auth.models import User
from django.utils.timezone import now,localtime

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
        
        #mark users as online when they connect
        await self.update_online_status(True)
            
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        

    async def disconnect(self, close_code):
        #mark users as offline when they disconnect
        await self.update_online_status(False,last_seen = now())
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
    async def update_online_status(self, is_online,last_seen = None):
        registration = await database_sync_to_async(Registration.objects.get)(user=self.user)
        registration.is_online = is_online
        if last_seen:
            registration.last_seen = last_seen
        await database_sync_to_async(registration.save)()

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender = self.scope["user"]
        receiver = await database_sync_to_async(User.objects.get)(id=self.other_user_id)
        message_obj = await database_sync_to_async(Message.objects.create)(
            room=self.room,
            sender=sender,
            receiver=receiver,
            message=message,
            sent_at= localtime(now())
        )
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_obj.message,
                'sender': message_obj.sender.username,
                'receiver':message_obj.receiver.username,
                'sent_at': message_obj.sent_at.isoformat()
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        receiver = event['receiver']
        sent_at = event['sent_at']
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'receiver': receiver,
            'sent_at': sent_at
        }))
        
