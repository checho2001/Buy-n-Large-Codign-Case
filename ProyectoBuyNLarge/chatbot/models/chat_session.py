import uuid
from django.db import models
from django.contrib.auth import get_user_model

#chat session model
class ChatSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=True,  # Permitir usuarios anónimos
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Sesión {self.id}"