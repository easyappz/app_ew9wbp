from rest_framework import generics, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import Message
from .serializers import MessageSerializer


class MessageListCreateView(generics.ListCreateAPIView):
    """
    API endpoint for listing all messages and creating new messages.
    GET: Returns all messages ordered by timestamp.
    POST: Creates a new message with username, message text, and user_color.
    """
    queryset = Message.objects.all().order_by('timestamp')
    serializer_class = MessageSerializer

    @extend_schema(
        responses={200: MessageSerializer(many=True)},
        description="Retrieve all chat messages ordered by timestamp."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        request=MessageSerializer,
        responses={201: MessageSerializer},
        description="Create a new chat message."
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
