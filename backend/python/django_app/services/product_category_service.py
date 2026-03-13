from django_app.models.product_category import ProductCategory
from django_app.repositories.product_category_repository import ProductCategoryRepository


class ProductCategoryService:

    @classmethod
    def create_category(cls, data: dict):

        if "title" not in data or not data["title"].strip():
            return {"error": "title is required"}

        category = ProductCategory(
            title=data["title"].strip(),
            description=data.get("description", "")
        )

        ProductCategoryRepository.create(category)

        return category.to_dict()

    @classmethod
    def list_categories(cls):
        categories = ProductCategoryRepository.list()
        return [c.to_dict() for c in categories]

    @classmethod
    def get_category(cls, category_id: str):

        category = ProductCategoryRepository.get(category_id)

        if not category:
            return None

        return category.to_dict()

    @classmethod
    def update_category(cls, category_id: str, data: dict):

        category = ProductCategoryRepository.get(category_id)

        if not category:
            return None

        if "title" in data:
            category.title = data["title"]

        if "description" in data:
            category.description = data["description"]

        ProductCategoryRepository.update(category)

        return category.to_dict()

    @classmethod
    def delete_category(cls, category_id: str):

        deleted = ProductCategoryRepository.delete(category_id)

        return deleted