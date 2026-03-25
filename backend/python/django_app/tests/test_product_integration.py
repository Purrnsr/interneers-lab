import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_app.settings")
django.setup()
import json
import unittest
from django.test import Client
from django.core.files.uploadedfile import SimpleUploadedFile

from django_app.models.product_category import ProductCategory
from django_app.models.product import Product


class TestProductIntegration(unittest.TestCase):

    def setUp(self):
        self.client = Client()
        # Clean DB before each test
        Product.objects.delete()
        ProductCategory.objects.delete()

        self.category = ProductCategory(
            title="Electronics",
            description="Test category"
        )
        self.category.save()

    def test_create_product_api(self):
        payload = {
            "name": "Mouse",
            "description": "Wireless mouse",
            "category": str(self.category.id),
            "price": 999.0,
            "brand": "Logitech",
            "quantity": 10
        }

        response = self.client.post(
            "/products/",
            data=json.dumps(payload),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json()["success"])

    def test_update_product_api(self):
        product = Product(
            name="Old Mouse",
            description="Old",
            category=self.category,
            price=500,
            brand="HP",
            quantity=5
        )
        product.save()

        payload = {"name": "Updated Mouse"}

        response = self.client.put(
            f"/products/{product.id}/",
            data=json.dumps(payload),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)

        product.reload()  #  FIXED
        self.assertEqual(product.name, "Updated Mouse")
        #  Clean DB before each test
        #Product.objects.delete()
        #ProductCategory.objects.delete()
