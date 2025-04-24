from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from users.models import Customer, Vendor, DeliveryAgent

# Test cases for user-related views including registration and login
class UserViewTests(TestCase):

    # Setup test client for making requests
    def setUp(self):
        self.client = Client()

    # Test customer registration view and user creation
    def test_customer_registration(self):
        response = self.client.post(reverse('customer_register'), {
            'username': 'cust1',
            'password': 'pass1234',
            'email': 'cust1@example.com',
            'address': '123 Street',
            'phone': '1234567890'
        })
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='cust1').exists())
        self.assertTrue(Customer.objects.filter(user__username='cust1').exists())

    # Test vendor registration view and user creation
    def test_vendor_registration(self):
        response = self.client.post(reverse('vendor_register'), {
            'username': 'vendor1',
            'password': 'pass1234',
            'store_name': 'VendorMart',
            'phone': '0987654321',
            'email': 'vendor1@example.com'
        })
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='vendor1').exists())
        self.assertTrue(Vendor.objects.filter(user__username='vendor1').exists())

    # Test delivery agent registration view and user creation
    def test_delivery_agent_registration(self):
        response = self.client.post(reverse('delivery_register'), {
            'username': 'agent1',
            'password': 'pass1234',
            'phone': '1231231234',
            'region': 'North'
        })
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='agent1').exists())
        self.assertTrue(DeliveryAgent.objects.filter(user__username='agent1').exists())

    # Test login and redirect for customer user
    def test_login_and_redirect_customer(self):
        user = User.objects.create_user(username='custlogin', password='pass')
        Customer.objects.create(user=user, address='A', phone='X')
        response = self.client.post(reverse('login'), {
            'username': 'custlogin',
            'password': 'pass'
        })
        self.assertRedirects(response, reverse('customer_dashboard'))

    # Test login and redirect for vendor user
    def test_login_and_redirect_vendor(self):
        user = User.objects.create_user(username='vendorlogin', password='pass')
        Vendor.objects.create(user=user, store_name='MyStore')
        response = self.client.post(reverse('login'), {
            'username': 'vendorlogin',
            'password': 'pass'
        })
        self.assertRedirects(response, reverse('vendor_dashboard'))

    # Test login and redirect for delivery agent user
    def test_login_and_redirect_delivery_agent(self):
        user = User.objects.create_user(username='agentlogin', password='pass')
        DeliveryAgent.objects.create(user=user, phone='111')
        response = self.client.post(reverse('login'), {
            'username': 'agentlogin',
            'password': 'pass'
        })
        self.assertRedirects(response, reverse('delivery_dashboard'))
