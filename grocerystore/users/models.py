from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(default='', blank=True)
    phone = models.CharField(max_length=15, default='', blank=True)

    def __str__(self):
        return self.user.username

class Vendor(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='vendor',
        blank=True  # Allows null during creation
    )
    store_name = models.CharField(max_length=100, default='New Store')
    phone = models.CharField(max_length=15, default='', blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.store_name
    
class DeliveryAgent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    region = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} ({self.region})"
