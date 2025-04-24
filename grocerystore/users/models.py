from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# Model representing a customer with user link, address, and phone number
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    address = models.TextField(default='', blank=True)
    phone = models.CharField(max_length=15, default='', blank=True)

    def __str__(self):
        return self.user.username

# Model representing a vendor with user link, store details, and status
class Vendor(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='vendor',
        blank=True,
        null=True
    )
    store_name = models.CharField(max_length=100, default='New Store')
    phone = models.CharField(max_length=15, default='', blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.store_name
    
# Model representing a delivery agent with user link, phone, and region
class DeliveryAgent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    region = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} ({self.region})"
