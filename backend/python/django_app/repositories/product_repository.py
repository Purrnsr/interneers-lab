from django_app.models.product import Product
from datetime import datetime

class ProductRepository:
    """
    Repository responsible for interacting with MongoDB using MongoEngine ORM.
    """

    @classmethod
    def create(cls, product: Product):
        product.save()
        return product

    @classmethod
    def get(cls, product_id: str):
        return Product.objects(id=product_id, is_deleted=False).first()

    @classmethod
    def list(cls):
        return Product.objects(is_deleted=False)

    @classmethod
    def update(cls, product: Product):
        product.save()
        return product

    @classmethod
    def delete(cls, product_id: str):
        result = Product.objects(id=product_id).update(set__is_deleted=True)
        return result > 0
    
    @classmethod
    def list_updated_after(cls, timestamp: str):
        """
        Return products updated after a given timestamp.
    """
        try:
            time = datetime.fromisoformat(timestamp)
        except ValueError:
            return []

        products = Product.objects(
        updated_at__gt=time,
        is_deleted=False
        )
        return list(products)