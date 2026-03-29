from parameterized import parameterized
from unittest.mock import patch
from django_app.services.product_service import ProductService
from django_app.models.product_category import ProductCategory
import unittest


class TestProductService(unittest.TestCase):

    @parameterized.expand([
        (-100, "price must be a positive number"),
        (0, "price must be a positive number"),
    ])
    @patch.object(ProductService, "repository")
    def test_create_product_invalid_price(
        self,
        price,
        expected_error,
        mock_repository
    ):
        mock_category = ProductCategory(title="Electronics")

        data = {
            "name": "Mouse",
            "description": "Wireless mouse",
            "category": mock_category,
            "price": price,
            "brand": "Logitech",
            "quantity": 10
        }

        result = ProductService.create_product(data)

        self.assertIn("error", result)
        self.assertEqual(result["error"], expected_error)
        mock_repository.create.assert_not_called()
        print("Running test with price:", price)