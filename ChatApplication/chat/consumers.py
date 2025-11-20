from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from django.contrib.auth.models import AnonymousUser
import json
from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get the authenticated user from the session
        self.user = self.scope["user"]
        
        # Check if user is authenticated
        if self.user == AnonymousUser():
            await self.close()
            return
        
        # Get both usernames from URL
        self.sender_username = self.scope['url_route']['kwargs']['sender_username']
        self.receiver_username = self.scope['url_route']['kwargs']['receiver_username']
        
        # Verify that the authenticated user matches the sender
        if self.user.username != self.sender_username:
            await self.close()
            return
        
        # Create a deterministic room name based on both users (sorted alphabetically)
        usernames = sorted([self.sender_username, self.receiver_username])
        self.room_group_name = f"chat_{'_'.join(usernames)}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        
        # Save to DB
        try:
            sender_user = await database_sync_to_async(User.objects.get)(username=self.sender_username)
            receiver_user = await database_sync_to_async(User.objects.get)(username=self.receiver_username)
            await self.save_message(sender_user, receiver_user, message)
        except User.DoesNotExist as e:
            # Handle case where user doesn't exist
            await self.send(text_data=json.dumps({
                "error": f"User does not exist: {str(e)}"
            }))
            return

        # Broadcast message to group (both sender and receiver will receive it)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message", 
                "message": message, 
                "sender": self.sender_username,
                "receiver": self.receiver_username
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"],
            "receiver": event["receiver"]
        }))

    @database_sync_to_async
    def save_message(self, sender, receiver, message):
        return Message.objects.create(sender=sender, receiver=receiver, content=message)
