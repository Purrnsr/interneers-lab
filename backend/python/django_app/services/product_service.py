from django_app.models.product import Product
from django_app.repositories.product_repository import ProductRepository
from typing import Dict, List
import uuid
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
          
        # Validate string fields
        string_fields = ["name", "description", "category", "brand"]
        for field in string_fields:
          if not isinstance(data[field], str) or not data[field].strip():
             return {"error": f"{field} must be a non-empty string"}
          
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