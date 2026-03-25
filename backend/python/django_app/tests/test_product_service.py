import unittest
from unittest.mock import patch, MagicMock

from django_app.services.product_service import ProductService
from django_app.models.product_category import ProductCategory


class TestProductService(unittest.TestCase):

    @patch.object(ProductService, "repository")
    @patch("django_app.services.product_service.Product")  #  THIS IS NEW
    def test_create_product_success(self, mock_product_class, mock_repository):

        mock_category = ProductCategory(title="Electronics")

        # Mock product instance
        mock_product_instance = MagicMock()
        mock_product_instance.to_dict.return_value = {
            "name": "Mouse",
            "price": 999.0
        }

        # When Product(...) is called → return mock instance
        mock_product_class.return_value = mock_product_instance

        data = {
            "name": "Mouse",
            "description": "Wireless mouse",
            "category": mock_category,
            "price": 999.0,
            "brand": "Logitech",
            "quantity": 10
        }

        result = ProductService.create_product(data)

        self.assertNotIn("error", result)
        self.assertEqual(result["name"], "Mouse")
    @patch.object(ProductService, "repository")
    @patch("django_app.services.product_service.Product")
    def test_create_product_invalid_price(self, mock_product_class, mock_repository):

        mock_category = ProductCategory(title="Electronics")

        data = {
        "name": "Mouse",
        "description": "Wireless mouse",
        "category": mock_category,
        "price": -100,   # invalid
        "brand": "Logitech",
        "quantity": 10
        }

        result = ProductService.create_product(data)

        self.assertIn("error", result)
        self.assertEqual(result["error"], "price must be a positive number")
    @patch.object(ProductService, "repository")
    def test_update_product_success(self, mock_repository):

        # Mock existing product
        mock_product = MagicMock()
        mock_product.is_deleted = False
        mock_product.to_dict.return_value = {
            "id": "123",
            "name": "Updated Mouse"
        }

        # repository.get() returns product
        mock_repository.get.return_value = mock_product

        data = {
            "name": "Updated Mouse"
        }

        result = ProductService.update_product("123", data)

        self.assertNotIn("error", result)
        self.assertEqual(result["name"], "Updated Mouse")
    @patch.object(ProductService, "repository")
    def test_update_product_not_found(self, mock_repository):

        # Simulate product not found
        mock_repository.get.return_value = None

        data = {
            "name": "Updated Mouse"
        }

        result = ProductService.update_product("123", data)

        self.assertIsNone(result)
    @patch.object(ProductService, "repository")
    @patch.object(ProductService, "category_repository")  #  NEW
    @patch("django_app.services.product_service.Product")
    def test_bulk_create_products_mixed(self, mock_product_class, mock_category_repo, mock_repository):

        from io import BytesIO

        # Mock product instance
        mock_product = MagicMock()
        mock_product.to_dict.return_value = {
            "name": "Mouse",
            "price": 999.0
        }
        mock_product_class.return_value = mock_product

        # Mock category lookup
        valid_category = ProductCategory(title="Electronics")

        mock_category_repo.list.return_value.filter.return_value.first.side_effect = [
            valid_category,  # first row valid
            None             # second row invalid
        ]

        #  FIXED CSV (no leading spaces)
        csv_data = """name,description,category,brand,price,quantity,
Mouse,Wireless mouse,Electronics,Logitech,999,10,
Keyboard,Mechanical keyboard,InvalidCategory,HP,1999,5"""

        file = BytesIO(csv_data.encode("utf-8"))

        result = ProductService.bulk_create_products(file)

        self.assertEqual(result["created_count"], 1)
        self.assertEqual(len(result["errors"]), 1)
        self.assertEqual(result["errors"][0]["error"], "Invalid category")
    @patch.object(ProductService, "repository")
    def test_get_product_not_found(self, mock_repo):
        mock_repo.get.return_value = None

        result = ProductService.get_product("123")

        self.assertIsNone(result)


    @patch.object(ProductService, "repository")
    def test_delete_product_not_found(self, mock_repo):
        mock_repo.delete.return_value = False

        result = ProductService.delete_product("123")

        self.assertIsNone(result)


    @patch.object(ProductService, "repository")
    def test_list_products_empty(self, mock_repo):
        mock_repo.list.return_value = []

        result = ProductService.list_products()

        self.assertEqual(result["total_items"], 0)


    @patch.object(ProductService, "repository")
    def test_filter_products_empty(self, mock_repo):
        mock_repo.filter_products.return_value = []

        result = ProductService.filter_products()

        self.assertEqual(result, [])


    @patch.object(ProductService, "category_repository")
    @patch.object(ProductService, "repository")
    def test_assign_product_to_category_invalid_category(self, mock_repo, mock_cat_repo):
        mock_cat_repo.get.return_value = None

        result = ProductService.assign_product_to_category("p1", "c1")

        self.assertIsNone(result)     