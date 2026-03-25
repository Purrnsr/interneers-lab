import json
import unittest
from unittest.mock import patch, MagicMock
from django.test import Client
import unittest
from unittest.mock import patch, MagicMock
from django_app.services.product_category_service import ProductCategoryService
from django_app.repositories.product_category_repository import ProductCategoryRepository
from django_app.models.product_category import ProductCategory


class ProductCategoryService:

    category_repository = ProductCategoryRepository

    @classmethod
    def create_category(cls, data):
        title = data.get("title")
        description = data.get("description")

        if not title or not title.strip():
            return {"error": "title is required"}

        category = ProductCategory(
            title=title.strip(),
            description=description
        )

        cls.category_repository.create(category)

        return category.to_dict()

    @classmethod
    def list_categories(cls):
        categories = cls.category_repository.list()
        return [c.to_dict() for c in categories]

    @classmethod
    def get_category(cls, category_id):
        category = cls.category_repository.get(category_id)
        return category.to_dict() if category else None

    @classmethod
    def update_category(cls, category_id, data):
        category = cls.category_repository.get(category_id)

        if not category:
            return None

        if "title" in data:
            category.title = data["title"]

        if "description" in data:
            category.description = data["description"]

        cls.category_repository.update(category)

        return category.to_dict()

    @classmethod
    def delete_category(cls, category_id):
        return cls.category_repository.delete(category_id)
    def test_create_category_none_title(self):
        result = ProductCategoryService.create_category({"title": None})
        self.assertIn("error", result)

    @patch.object(ProductCategoryService, "category_repository")
    def test_list_categories_empty(self, mock_repo):
        mock_repo.list.return_value = []

        result = ProductCategoryService.list_categories()

        self.assertEqual(result, [])