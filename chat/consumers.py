# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from django.core.exceptions import ObjectDoesNotExist
from .models import Conversation, Message
from account.models import CustomUser

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            # Extract and validate JWT token
            token = self.scope['query_string'].decode().split('token=')[1]
            self.user = await self.get_user(token)
            
            if isinstance(self.user, AnonymousUser):
                await self.close()
                return

            # Get conversation ID from URL route
            self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
            self.room_group_name = f'chat_{self.conversation_id}'

            # Verify user is conversation participant
            if not await self.is_participant():
                await self.close()
                return

            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

        except (IndexError, KeyError, ObjectDoesNotExist) as e:
            await self.close()

    @database_sync_to_async
    def get_user(self, token):
        try:
            access_token = AccessToken(token)
            user_id = access_token.payload.get('user_id')
            return CustomUser.objects.get(id=user_id)
        except Exception:
            return AnonymousUser()

    @database_sync_to_async
    def is_participant(self):
        return Conversation.objects.filter(
            id=self.conversation_id,
            participants=self.user
        ).exists()

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message_content = text_data_json.get('message', '').strip()
            
            if message_content:
                message = await self.create_message(message_content)
                await self.broadcast_message(message)

        except json.JSONDecodeError:
            pass  # Handle invalid JSON format

    @database_sync_to_async
    def create_message(self, content):
        conversation = Conversation.objects.get(id=self.conversation_id)
        return Message.objects.create(
            conversation=conversation,
            sender=self.user,
            content=content,
            read=False
        )

    async def broadcast_message(self, message):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': {
                    'id': message.id,
                    'sender': await self.get_sender_data(),
                    'content': message.content,
                    'created_at': message.created_at.isoformat(),
                    'read': message.read
                }
            }
        )

    @database_sync_to_async
    def get_sender_data(self):
        return {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'profile_image': self.user.profile.profile_image.url if (
                hasattr(self.user, 'profile') and 
                self.user.profile.profile_image
            ) else None
        }

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event['message']))
