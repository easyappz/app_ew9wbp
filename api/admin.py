from django.contrib import admin
from .models import ChatMessage


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['username', 'message', 'timestamp']
    list_filter = ['timestamp', 'username']
    search_fields = ['username', 'message']
    readonly_fields = ['timestamp']
    ordering = ['-timestamp']