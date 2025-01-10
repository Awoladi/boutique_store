# products/tests/test_models.py
from django.test import TestCase
from .models import Product, Category

class ProductModelTest(TestCase):

    def setUp(self):
        category = Category.objects.create(name="Books")
        Product.objects.create(name="Test Book", price=20, stock=5, category=category)

    def test_product_creation(self):
        """Test if the product is correctly created"""
        product = Product.objects.get(name="Test Book")
        self.assertEqual(product.price, 20)
        self.assertEqual(product.stock, 5)
