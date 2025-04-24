from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from users.models import Customer, Vendor
from products.models import Product
from orders.models import Order, OrderDetail


class OrderViewTests(TestCase):

    def setUp(self):
        # Set up test client and create test user, customer, vendor, and product
        self.client = Client()
        self.user = User.objects.create_user(username='cust1', password='testpass')
        self.customer = Customer.objects.create(user=self.user, address='Test St', phone='123456')
        self.vendor = Vendor.objects.create(user=self.user, store_name='Test Store', phone='1234567890')
        self.product = Product.objects.create(name='Apple', price=1.50, stock=10, category='Fruits', vendor=self.vendor)
        self.client.login(username='cust1', password='testpass')

    def test_cart_view(self):
        """Test that the cart view displays products in the cart."""
        session = self.client.session
        session['cart'] = {str(self.product.id): 2}
        session.save()

        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Apple')

    def test_add_to_cart(self):
        """Test adding a product to the cart."""
        response = self.client.get(reverse('add_to_cart', args=[self.product.id]))
        self.assertRedirects(response, reverse('cart'))
        session = self.client.session
        self.assertIn(str(self.product.id), session['cart'])

    def test_remove_from_cart(self):
        """Test removing a product from the cart."""
        session = self.client.session
        session['cart'] = {str(self.product.id): 1}
        session.save()

        response = self.client.get(reverse('remove_from_cart', args=[self.product.id]))
        self.assertRedirects(response, reverse('cart'))
        session = self.client.session
        self.assertNotIn(str(self.product.id), session['cart'])

    def test_checkout_creates_order(self):
        """Test that checkout creates an order and redirects to success page."""
        session = self.client.session
        session['cart'] = {str(self.product.id): 2}
        session.save()

        response = self.client.post(reverse('checkout'), {
            'delivery_address': 'New Delivery Address',
            'payment_method': 'Card'
        })

        self.assertRedirects(response, reverse('order_success'))
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.customer, self.customer)
        self.assertEqual(order.delivery_address, 'New Delivery Address')
        self.assertEqual(order.payment_method, 'Card')

    def test_order_success_view(self):
        """Test the order success confirmation page."""
        response = self.client.get(reverse('order_success'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Order Placed Successfully')

    def test_order_history_view(self):
        """Test the order history page displays orders."""
        order = Order.objects.create(
            customer=self.customer,
            status='Delivered',
            delivery_address='Test St',
            payment_method='Card'
        )
        response = self.client.get(reverse('order_history'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Delivered')

    def test_track_order_view(self):
        """Test tracking a specific order."""
        order = Order.objects.create(
            customer=self.customer,
            status='Out for Delivery',
            delivery_address='123 Test',
            payment_method='COD'
        )
        response = self.client.get(reverse('track_order', args=[order.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Out for Delivery')
