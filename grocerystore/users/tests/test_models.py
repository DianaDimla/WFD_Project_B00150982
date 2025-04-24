from django.test import TestCase
from django.contrib.auth.models import User
from users.models import Customer, Vendor, DeliveryAgent
from django.utils import timezone

# Test cases for user-related models: Customer, Vendor, DeliveryAgent
class UserModelTests(TestCase):

    # Test creation and string representation of Customer model
    def test_customer_creation_and_str(self):
        user = User.objects.create_user(username='cust1', password='pass')
        customer = Customer.objects.create(user=user, address='123 Test St', phone='1234567890')
        
        self.assertEqual(customer.user.username, 'cust1')
        self.assertEqual(customer.address, '123 Test St')
        self.assertEqual(str(customer), 'cust1')

    # Test creation and string representation of Vendor model
    def test_vendor_creation_and_str(self):
        user = User.objects.create_user(username='vendor1', password='pass')
        vendor = Vendor.objects.create(user=user, store_name='Test Store', phone='5555555')

        self.assertEqual(vendor.store_name, 'Test Store')
        self.assertTrue(vendor.is_active)
        self.assertEqual(str(vendor), 'Test Store')

    # Test creation and string representation of DeliveryAgent model
    def test_delivery_agent_creation_and_str(self):
        user = User.objects.create_user(username='agent1', password='pass')
        delivery_agent = DeliveryAgent.objects.create(user=user, phone='9999999', region='North')

        self.assertEqual(delivery_agent.user.username, 'agent1')
        self.assertEqual(delivery_agent.region, 'North')
        self.assertEqual(str(delivery_agent), 'agent1 (North)')
