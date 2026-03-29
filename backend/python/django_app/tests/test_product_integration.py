
import json
from django.test import TestCase
from django.test import Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django_app.models.product_category import ProductCategory
from django_app.models.product import Product


class TestProductIntegration(TestCase):

    def setUp(self):
        self.client = Client()
        # Clean DB before each test
        Product.objects.delete() 
        ProductCategory.objects.delete()
        call_command("seed_categories")
        self.category = ProductCategory.objects(title="Electronics").first()
        self.assertIsNotNone(self.category)
        

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
        #DB validation
        self.assertEqual(Product.objects.count(),1)

        product = Product.objects.first()

        self.assertEqual(product.name, "Mouse")
        self.assertEqual(product.price, 999.0)
        self.assertEqual(product.brand, "Logitech")
        self.assertEqual(product.quantity, 10)

        # mongo engine object comparison

        self.assertEqual(str(product.category.id),str(self.category.id))
    def test_create_product_missing_name(self):
        payload = {
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

        self.assertEqual(response.status_code, 400)


        self.assertEqual(response.status_code, 400)
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
