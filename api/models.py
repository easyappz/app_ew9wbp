from django.db import models


class ChatMessage(models.Model):
    username = models.CharField(max_length=100)
    user_color = models.CharField(max_length=7)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.username}: {self.message[:50]}"