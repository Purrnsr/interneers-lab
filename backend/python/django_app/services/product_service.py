from django_app.models.product import Product
from django_app.repositories.product_repository import ProductRepository
from typing import Dict, List
import uuid
from django_app.repositories.product_category_repository import ProductCategoryRepository
from django_app.models.product_category import ProductCategory

class ProductService:
    """
    Service layer responsible for product business logic.
    In-memory storage for Week 2.
    """
    @classmethod
    def create_product(cls, data: dict) -> dict:
        """
        Create a new product.
        """
         
        # Basic validation
        required_fields = ["name", "description", "category", "price", "brand", "quantity"]

        # Check required fields
        for field in required_fields:
          if field not in data:
             return {"error": f"{field} is required"}
        if "brand" not in data or not data["brand"].strip():
            return {"error": "brand is required"}
        # Validate string fields
        string_fields = ["name", "description",  "brand"]
        for field in string_fields:
          if not isinstance(data[field], str) or not data[field].strip():
             return {"error": f"{field} must be a non-empty string"}
          
        if "category" not in data or not isinstance(data["category"], ProductCategory):
            return {"error": "category must be a valid category"}
        # Validate price
        if not isinstance(data["price"], (int, float)) or data["price"] <= 0:
          return {"error": "price must be a positive number"}


        #Validate quantity
        if not isinstance(data["quantity"], int) or data["quantity"] < 0:
          return {"error": "quantity must be a non-negative integer"}

        product = Product(
            name=data["name"],
            description=data["description"],
            category=data["category"],
            price=data["price"],
            brand=data["brand"],
            quantity=data["quantity"],
        )

        ProductRepository.create(product)
        return product.to_dict()

    @classmethod
    def get_product(cls, product_id: str) -> dict:
        product = ProductRepository.get(product_id)

        if not product or product.is_deleted:
            return None

        return product.to_dict()

    @classmethod
    def list_products(cls, page: int = 1, page_size: int = 10) -> List[dict]:
        active_products = [
        product.to_dict()
        for product in ProductRepository.list()
        if not product.is_deleted
        ]

        total_items = len(active_products)
        total_pages = (total_items + page_size - 1) // page_size  # ceiling division

        # Pagination logic
        start = (page - 1) * page_size
        end = start + page_size

        paginated = active_products[start:end]

        return {
        "page": page,
        "page_size": page_size,
        "total_items": total_items,
        "total_pages": total_pages,
        "data": paginated
        }

    @classmethod
    def update_product(cls, product_id: str, data: dict) -> dict:
        product = ProductRepository.get(product_id)
        if not product or product.is_deleted:
            return None

    # Validate and update allowed fields only

        if "name" in data:
            if not isinstance(data["name"], str) or not data["name"].strip():
                return {"error": "name must be a non-empty string"}
            product.name = data["name"].strip()

        if "description" in data:
            if not isinstance(data["description"], str) or not data["description"].strip():
                return {"error": "description must be a non-empty string"}
            product.description = data["description"].strip()

        if "category" in data:
            if not isinstance(data["category"], str) or not data["category"].strip():
                return {"error": "category must be a non-empty string"}
            product.category = data["category"].strip()

        if "brand" in data:
            if not isinstance(data["brand"], str) or not data["brand"].strip():
                return {"error": "brand must be a non-empty string"}
            product.brand = data["brand"].strip()

        if "price" in data:
            if not isinstance(data["price"], (int, float)) or data["price"] <= 0:
                return {"error": "price must be a positive number"}
            product.price = data["price"]

        if "quantity" in data:
            if not isinstance(data["quantity"], int) or data["quantity"] < 0:
                return {"error": "quantity must be a non-negative integer"}
            product.quantity = data["quantity"]

        ProductRepository.update(product)
        return product.to_dict()

    @classmethod
    def delete_product(cls, product_id: str):
        deleted = ProductRepository.delete(product_id)
        if not deleted:
         return None
        return {"message": "Product deleted successfully"}
    @classmethod
    def list_products_updated_after(cls, timestamp: str):
        products = ProductRepository.list_updated_after(timestamp)

        return [product.to_dict() for product in products]
    @classmethod
    def get_products_by_category(cls, category_id: str):

        products = ProductRepository.get_products_by_category(category_id)

        if products is None:
            return None

        return [p.to_dict() for p in products]
    @classmethod
    def assign_product_to_category(cls, product_id: str, category_id: str):

        category = ProductCategoryRepository.get(category_id)

        if not category:
            return None

        product = ProductRepository.assign_category(product_id, category)

        if not product:
            return False

        return product.to_dict()
    
    @classmethod
    def remove_product_from_category(cls, product_id: str):

        product = ProductRepository.remove_category(product_id)

        if not product:
            return None

        return product.to_dict()
    
    @classmethod
    def filter_products(cls, category=None, price_min=None, price_max=None):

        category_titles = None

        if category:
            category_titles = [c.strip() for c in category.split(",")]

        products = ProductRepository.filter_products(
            category_titles=category_titles,
            price_min=price_min,
            price_max=price_max
        )

        return [p.to_dict() for p in products]