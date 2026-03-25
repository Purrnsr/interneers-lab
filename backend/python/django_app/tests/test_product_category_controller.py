import json
import unittest
from unittest.mock import patch

from django.test import Client


class TestProductCategoryController(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    @patch("django_app.services.product_category_service.ProductCategoryService.create_category")
    def test_create_category_success(self, mock_create):
        mock_create.return_value = {"title": "Electronics"}

        response = self.client.post(
            "/categories/",
            data=json.dumps({"title": "Electronics"}),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)

    def test_create_category_invalid_json(self):
        response = self.client.post(
            "/categories/",
            data="INVALID",
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)

    @patch("django_app.services.product_category_service.ProductCategoryService.get_category")
    def test_get_category_not_found(self, mock_get):
        mock_get.return_value = None

        response = self.client.get("/categories/123/")

        self.assertEqual(response.status_code, 404)

    @patch("django_app.services.product_category_service.ProductCategoryService.delete_category")
    def test_delete_category_not_found(self, mock_delete):
        mock_delete.return_value = False

        response = self.client.delete("/categories/123/")

        self.assertEqual(response.status_code, 404)