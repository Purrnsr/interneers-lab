import json
import unittest
from unittest.mock import patch

from django.test import Client


class TestProductController(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    @patch("django_app.services.product_service.ProductService.create_product")
    def test_create_product_success(self, mock_create):
        mock_create.return_value = {"name": "Mouse"}

        payload = {
            "name": "Mouse",
            "description": "Wireless mouse",
            "category": "123",
            "price": 999,
            "brand": "Logitech",
            "quantity": 10
        }

        response = self.client.post(
            "/products/",
            data=json.dumps(payload),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)

    def test_create_product_invalid_json(self):
        response = self.client.post(
            "/products/",
            data="INVALID_JSON",
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)

    @patch("django_app.services.product_service.ProductService.get_product")
    def test_get_product_not_found(self, mock_get):
        mock_get.return_value = None

        response = self.client.get("/products/123/")

        self.assertEqual(response.status_code, 404)

    @patch("django_app.services.product_service.ProductService.update_product")
    def test_update_product_missing_id(self, mock_update):
        response = self.client.put(
            "/products/",
            data=json.dumps({"name": "New"}),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)

    @patch("django_app.services.product_service.ProductService.delete_product")
    def test_delete_product_not_found(self, mock_delete):
        mock_delete.return_value = None

        response = self.client.delete("/products/123/")

        self.assertEqual(response.status_code, 404)