from django.db import models
from users.models import Customer
from products.models import Product

# Model representing a customer's order
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=50, default="Pending")
    delivery_agent = models.ForeignKey('users.DeliveryAgent', null=True, blank=True, on_delete=models.SET_NULL)
    delivery_address = models.TextField(blank=True, null=True)
    payment_method = models.CharField(max_length=50, choices=[
    ('Card', 'Credit/Debit Card'),
    ('COD', 'Cash on Delivery')
    ], default='Card')


    def __str__(self):
        return f"Order #{self.id} by {self.customer.user.username}"

# Model representing details of products in an order
class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='details')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_at_purchase = models.DecimalField(max_digits=8, decimal_places=2)
    fulfilled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

# Model representing payment information for an order
class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_method = models.CharField(max_length=30)
    payment_status = models.CharField(max_length=30)

    def __str__(self):
        return f"Payment for Order #{self.order.id}"
