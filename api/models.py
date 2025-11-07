from django.db import models


class Message(models.Model):
    """
    Model to store chat messages.
    """
    username = models.CharField(max_length=100)
    message = models.TextField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    user_color = models.CharField(max_length=7)

    class Meta:
        ordering = ['timestamp']
        indexes = [
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f"{self.username}: {self.message[:50]}"
