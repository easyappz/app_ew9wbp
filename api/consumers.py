import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone


class ChatConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for chat functionality.
    Handles real-time messaging, online count, and typing indicators.
    """

    async def connect(self):
        """Handle WebSocket connection."""
        self.room_group_name = "chat_room"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Increment and broadcast online count
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "user_count_update",
                "action": "increment"
            }
        )

    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        # Decrement and broadcast online count
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "user_count_update",
                "action": "decrement"
            }
        )

    async def receive(self, text_data):
        """Receive message from WebSocket."""
        try:
            data = json.loads(text_data)
            message_type = data.get("type")

            if message_type == "chat_message":
                await self.handle_chat_message(data)
            elif message_type == "typing":
                await self.handle_typing(data)
        except json.JSONDecodeError:
            pass

    async def handle_chat_message(self, data):
        """Handle incoming chat message."""
        message_text = data.get("message", "")
        username = data.get("username", "Guest")
        user_color = data.get("user_color", "#000000")

        if not message_text:
            return

        # Save message to database
        message_data = await self.save_message(username, message_text, user_color)

        # Broadcast message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message_broadcast",
                "message": message_data
            }
        )

    async def handle_typing(self, data):
        """Handle typing indicator."""
        username = data.get("username", "Guest")
        is_typing = data.get("is_typing", False)

        # Broadcast typing status to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "typing_indicator",
                "username": username,
                "is_typing": is_typing,
                "sender_channel": self.channel_name
            }
        )

    async def chat_message_broadcast(self, event):
        """Send chat message to WebSocket."""
        message = event["message"]

        await self.send(text_data=json.dumps({
            "type": "chat_message",
            "message": message
        }))

    async def typing_indicator(self, event):
        """Send typing indicator to WebSocket."""
        # Don't send typing indicator back to sender
        if event.get("sender_channel") == self.channel_name:
            return

        await self.send(text_data=json.dumps({
            "type": "typing",
            "username": event["username"],
            "is_typing": event["is_typing"]
        }))

    async def user_count_update(self, event):
        """Send online count update to WebSocket."""
        # This is a simplified implementation
        # In production, you would track actual connected users
        await self.send(text_data=json.dumps({
            "type": "online_count",
            "action": event["action"]
        }))

    @database_sync_to_async
    def save_message(self, username, message_text, user_color):
        """Save message to database."""
        from api.models import ChatMessage

        message = ChatMessage.objects.create(
            username=username,
            message=message_text,
            user_color=user_color
        )

        return {
            "id": message.id,
            "username": message.username,
            "message": message.message,
            "user_color": message.user_color,
            "timestamp": message.timestamp.isoformat()
        }
