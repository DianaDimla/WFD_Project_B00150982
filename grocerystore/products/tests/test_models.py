from django.test import TestCase
from django.contrib.auth.models import User
from users.models import Vendor
from products.models import Product

# Test cases for Product model
class ProductModelTest(TestCase):

    # Setup test data: vendor and product
    def setUp(self):
        # Create a vendor user
        self.user = User.objects.create_user(username='vendoruser', password='testpass')
        self.vendor = Vendor.objects.create(user=self.user, store_name='Test Vendor')

        # Create a product
        self.product = Product.objects.create(
            name='Organic Banana',
            description='Fresh organic bananas from local farms.',
            price=1.99,
            category='Fruits',
            stock=100,
            vendor=self.vendor
        )

    # Test string representation of Product
    def test_product_str(self):
        """Test the string representation of the Product model."""
        self.assertEqual(str(self.product), 'Organic Banana')

    # Test product price field
    def test_product_price(self):
        """Ensure the product price is stored correctly."""
        self.assertEqual(self.product.price, 1.99)

    # Test product category field
    def test_product_category(self):
        """Check that the product category is assigned correctly."""
        self.assertEqual(self.product.category, 'Fruits')

    # Test product stock is non-negative
    def test_product_stock_is_positive(self):
        """Stock should be greater than or equal to zero."""
        self.assertGreaterEqual(self.product.stock, 0)

    # Test product-vendor relationship
    def test_product_vendor_relation(self):
        """Product should be linked to the correct vendor."""
        self.assertEqual(self.product.vendor.store_name, 'Test Vendor')
        self.assertEqual(self.product.vendor.user.username, 'vendoruser')
