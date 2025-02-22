from django.db import models
from .chat_session import ChatSession
from inventory.models import Product

class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE)
    message_text = models.TextField()
    is_bot = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['session']),
        ]

    def __str__(self):
        return f"Mensaje {self.id} - {'Bot' if self.is_bot else 'Usuario'}"