import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatMessage
from .serializers import ChatMessageSerializer


class ChatConsumer(AsyncWebsocketConsumer):
    room_group_name = 'chat_room'
    connected_users = set()

    async def connect(self):
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        
        self.connected_users.add(self.channel_name)
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'online_count',
                'count': len(self.connected_users)
            }
        )

    async def disconnect(self, close_code):
        if self.channel_name in self.connected_users:
            self.connected_users.remove(self.channel_name)
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'online_count',
                'count': len(self.connected_users)
            }
        )
        
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')

        if message_type == 'chat_message':
            username = data.get('username')
            user_color = data.get('user_color')
            message = data.get('message')

            chat_message = await self.save_message(username, user_color, message)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'id': chat_message['id'],
                    'username': chat_message['username'],
                    'user_color': chat_message['user_color'],
                    'message': chat_message['message'],
                    'timestamp': chat_message['timestamp']
                }
            )

        elif message_type == 'typing':
            username = data.get('username')
            is_typing = data.get('is_typing', False)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'typing_indicator',
                    'username': username,
                    'is_typing': is_typing,
                    'sender_channel': self.channel_name
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'id': event['id'],
            'username': event['username'],
            'user_color': event['user_color'],
            'message': event['message'],
            'timestamp': event['timestamp']
        }))

    async def typing_indicator(self, event):
        if event['sender_channel'] != self.channel_name:
            await self.send(text_data=json.dumps({
                'type': 'typing',
                'username': event['username'],
                'is_typing': event['is_typing']
            }))

    async def online_count(self, event):
        await self.send(text_data=json.dumps({
            'type': 'online_count',
            'count': event['count']
        }))

    @database_sync_to_async
    def save_message(self, username, user_color, message):
        chat_message = ChatMessage.objects.create(
            username=username,
            user_color=user_color,
            message=message
        )
        serializer = ChatMessageSerializer(chat_message)
        return serializer.data