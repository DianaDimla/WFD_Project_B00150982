from django.db import models
from users.models import Vendor
from django.core.validators import MinValueValidator

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default='')
    price = models.DecimalField(
        max_digits=8, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    category = models.CharField(max_length=50, default='general')
    stock = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    vendor = models.ForeignKey(
        Vendor, 
        on_delete=models.CASCADE,
        related_name='products'
    )

    def __str__(self):
        return self.name