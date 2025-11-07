from rest_framework import serializers
from .models import ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'username', 'user_color', 'message', 'timestamp']
        read_only_fields = ['id', 'timestamp']