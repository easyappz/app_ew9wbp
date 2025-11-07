from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Message model.
    """
    class Meta:
        model = Message
        fields = ['id', 'username', 'message', 'timestamp', 'user_color']
        read_only_fields = ['id', 'timestamp']

    def validate_message(self, value):
        """
        Validate that message is not empty and within length limit.
        """
        if not value or not value.strip():
            raise serializers.ValidationError("Message cannot be empty.")
        if len(value) > 1000:
            raise serializers.ValidationError("Message cannot exceed 1000 characters.")
        return value.strip()

    def validate_username(self, value):
        """
        Validate username is not empty.
        """
        if not value or not value.strip():
            raise serializers.ValidationError("Username cannot be empty.")
        return value.strip()

    def validate_user_color(self, value):
        """
        Validate that user_color is a valid hex color code.
        """
        if not value or not value.startswith('#') or len(value) != 7:
            raise serializers.ValidationError("User color must be a valid hex color code (e.g., #FF5733).")
        return value
