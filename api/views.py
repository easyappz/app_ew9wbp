from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import ChatMessage
from .serializers import ChatMessageSerializer


class ChatMessageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return ChatMessage.objects.all().order_by('timestamp')