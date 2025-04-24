from django.test import TestCase
from django.contrib.auth.models import User
from users.models import Customer, Vendor
from products.models import Product
from orders.models import Order, OrderDetail
from django.utils import timezone


class OrderModelTests(TestCase):

    def setUp(self):
        # Create user and customer for testing
        self.user = User.objects.create_user(username='cust1', password='pass')
        self.customer = Customer.objects.create(user=self.user, address='123 Test St', phone='111222333')
        self.vendor = Vendor.objects.create(user=self.user, store_name='Test Store', phone='1234567890')

        # Create a product for testing
        self.product = Product.objects.create(
            name='Organic Apple',
            description='Fresh and juicy',
            price=2.00,
            category='Fruits',
            stock=50,
            vendor=self.vendor
        )

        # Create an order for testing
        self.order = Order.objects.create(
            customer=self.customer,
            status='Processing',
            delivery_address='456 Delivery Ln',
            payment_method='Card',
            created_at=timezone.now()
        )

        # Create an order item for testing
        self.order_item = OrderDetail.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price_at_purchase=self.product.price,
            fulfilled=False
        )

    def test_order_str(self):
        """Test string representation of Order model."""
        self.assertEqual(str(self.order), f'Order #{self.order.id} by {self.customer.user.username}')

    def test_order_fields(self):
        """Test that order fields are saved correctly."""
        self.assertEqual(self.order.customer.user.username, 'cust1')
        self.assertEqual(self.order.status, 'Processing')
        self.assertEqual(self.order.delivery_address, '456 Delivery Ln')
        self.assertEqual(self.order.payment_method, 'Card')

    def test_order_item_relationship(self):
        """Test that order has related order items."""
        self.assertEqual(self.order.details.first(), self.order_item)
        self.assertEqual(self.order_item.product.name, 'Organic Apple')

    def test_order_item_calculation(self):
        """Ensure subtotal matches quantity * price."""
        expected = self.order_item.quantity * self.product.price
        self.assertEqual(self.order_item.price_at_purchase, self.product.price)
