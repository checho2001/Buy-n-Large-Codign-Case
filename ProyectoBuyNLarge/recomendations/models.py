from django.db import models
from users.models import CustomUser
from inventory.models import Product

class Recommendation(models.Model):
    
    CATEGORY_CHOICES = [
        ('Altamente Recomendado', 'Altamente Recomendado'),
        ('Recomendado', 'Recomendado'),
        ('No Recomendado', 'No Recomendado'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=3, decimal_places=2)  # Ej: 0.95
    category = models.CharField(max_length=25, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['user']),
        ]

    def _str_(self):
        return f"Recomendación para {self.user.username} - {self.product.name}"