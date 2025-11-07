from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """
    Admin interface for Message model.
    """
    list_display = ['id', 'username', 'message_preview', 'timestamp', 'user_color']
    list_filter = ['timestamp', 'username']
    search_fields = ['username', 'message']
    readonly_fields = ['timestamp']
    ordering = ['-timestamp']

    def message_preview(self, obj):
        """
        Display a preview of the message in the admin list.
        """
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Message'
