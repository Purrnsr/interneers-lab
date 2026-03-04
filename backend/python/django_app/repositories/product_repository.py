from typing import Dict, List
from django_app.models.product import Product

class ProductRepository:
    """
    Repository layer responsible for data storage and retrieval.
    Currently uses in-memory storage.
    """

    _products: Dict[str, Product] = {}

    @classmethod
    def create(cls, product: Product) -> Product:
        cls._products[product.id] = product
        return product

    @classmethod
    def get(cls, product_id: str) -> Product | None:
        return cls._products.get(product_id)

    @classmethod
    def list(cls) -> List[Product]:
        return list(cls._products.values())

    @classmethod
    def update(cls, product: Product) -> Product:
        cls._products[product.id] = product
        return product

    @classmethod
    def delete(cls, product_id: str) -> bool:
        product = cls._products.get(product_id)

        if not product or product.is_deleted:
            return False

        product.is_deleted = True
        return True