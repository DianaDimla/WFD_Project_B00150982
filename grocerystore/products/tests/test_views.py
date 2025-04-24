from django.test import TestCase, Client
from django.contrib.auth.models import User
from users.models import Vendor
from products.models import Product
from django.urls import reverse


class ProductViewTests(TestCase):

    def setUp(self):
        self.client = Client()

        # Create a vendor and log them in
        self.user = User.objects.create_user(username='vendor1', password='pass')
        self.vendor = Vendor.objects.create(user=self.user, store_name='Test Vendor')
        self.client.login(username='vendor1', password='pass')

        # Create a product
        self.product = Product.objects.create(
            name='Organic Tomato',
            description='Fresh tomatoes.',
            price=2.50,
            category='Vegetables',
            stock=30,
            vendor=self.vendor
        )

    def test_browse_products_view(self):
        """Test the customer-facing product listing page."""
        response = self.client.get(reverse('browse_products'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Organic Tomato')

    def test_vendor_inventory_view(self):
        """Test the vendor inventory dashboard."""
        response = self.client.get(reverse('vendor_inventory'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Organic Tomato')

    def test_edit_product_view_get(self):
        """Test accessing the edit product form."""
        url = reverse('edit_product', args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Organic Tomato')

    def test_edit_product_view_post(self):
        """Test submitting the edit product form."""
        url = reverse('edit_product', args=[self.product.id])
        response = self.client.post(url, {
            'name': 'Updated Tomato',
            'description': 'Red, ripe tomatoes.',
            'price': 3.00,
            'category': 'Vegetables',
            'stock': 25
        })
        self.assertRedirects(response, reverse('vendor_inventory'))
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Tomato')
        self.assertEqual(self.product.price, 3.00)
