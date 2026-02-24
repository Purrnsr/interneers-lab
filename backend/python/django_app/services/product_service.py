from typing import Dict, List
import uuid


class ProductService:
    """
    Service layer responsible for product business logic.
    In-memory storage for Week 2.
    """

    # In-memory data store
    _products: Dict[str, dict] = {}

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

        product_id = str(uuid.uuid4())

        product = {
        "id": product_id,
        "name": data["name"].strip(),
        "description": data["description"].strip(),
        "category": data["category"].strip(),
        "price": data["price"],
        "brand": data["brand"].strip(),
        "quantity": data["quantity"],
    }

        cls._products[product_id] = product
        return product

    @classmethod
    def get_product(cls, product_id: str) -> dict:
        return cls._products.get(product_id)

    @classmethod
    def list_products(cls) -> List[dict]:
        return list(cls._products.values())

    @classmethod
    def update_product(cls, product_id: str, data: dict) -> dict:
        if product_id not in cls._products:
            return None

        cls._products[product_id].update(data)
        return cls._products[product_id]

    @classmethod
    def delete_product(cls, product_id: str) -> bool:
        if product_id in cls._products:
            del cls._products[product_id]
            return True
        return False