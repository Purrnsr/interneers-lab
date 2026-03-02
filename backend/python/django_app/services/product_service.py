from typing import Dict, List
import uuid

class Product:
    def __init__(self, name: str, description: str, category: str,
                 price: float, brand: str, quantity: int):
        self.id = str(uuid.uuid4())
        self.name = name.strip()
        self.description = description.strip()
        self.category = category.strip()
        self.price = price
        self.brand = brand.strip()
        self.quantity = quantity
        self.is_deleted = False   # for soft delete

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "price": self.price,
            "brand": self.brand,
            "quantity": self.quantity,
        }
class ProductService:
    """
    Service layer responsible for product business logic.
    In-memory storage for Week 2.
    """

    # In-memory data store
    _products: Dict[str, Product] = {}

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

        cls._products[product.id] = product
        return product.to_dict()

    @classmethod
    def get_product(cls, product_id: str) -> dict:
        product = cls._products.get(product_id)

        if not product or product.is_deleted:
            return None

        return product.to_dict()

    @classmethod
    def list_products(cls) -> List[dict]:
        return [
            product.to_dict()
            for product in cls._products.values()
            if not product.is_deleted
        ]

    @classmethod
    def update_product(cls, product_id: str, data: dict) -> dict:
        product = cls._products.get(product_id)

        if not product or product.is_deleted:
            return None

        # Update allowed fields only
        if "name" in data:
            product.name = data["name"].strip()

        if "description" in data:
            product.description = data["description"].strip()

        if "category" in data:
            product.category = data["category"].strip()

        if "price" in data:
            product.price = data["price"]

        if "brand" in data:
            product.brand = data["brand"].strip()

        if "quantity" in data:
            product.quantity = data["quantity"]

        return product.to_dict()

    @classmethod
    def delete_product(cls, product_id: str):
        product = cls._products.get(product_id)

        if not product or product.is_deleted:
            return None

        product.is_deleted = True
        return product.to_dict()