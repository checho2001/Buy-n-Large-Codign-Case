from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, max_length=254)
    preferences = models.JSONField(default=dict, blank=True)  # Ej: {"brands": ["HP"], "categories": ["computers"]}
    last_login = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return self.username