from django_app.models.product import Product
from datetime import datetime
from django_app.models.product_category import ProductCategory

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
    @classmethod
    def get_products_by_category(cls, category_id: str):

        category = ProductCategory.objects(id=category_id).first()

        if not category:
            return None

        products = Product.objects(
             category=category,
            is_deleted=False
        )

        return list(products)
    @classmethod
    def assign_category(cls, product_id: str, category):

        product = Product.objects(id=product_id, is_deleted=False).first()

        if not product:
            return None

        product.category = category
        product.save()

        return product
    @classmethod
    def remove_category(cls, product_id: str):

        product = Product.objects(id=product_id, is_deleted=False).first()

        if not product:
            return None

        product.category = None
        product.save()

        return product
    
    @classmethod
    def filter_products(cls, category_titles=None, price_min=None, price_max=None):

        from django_app.models.product import Product
        from django_app.models.product_category import ProductCategory

        query = Product.objects(is_deleted=False)

        if category_titles:
            categories = list(ProductCategory.objects(title__in=category_titles))
            query = query.filter(category__in=categories)

        if price_min is not None:
            query = query.filter(price__gte=price_min)

        if price_max is not None:
            query = query.filter(price__lte=price_max)

        return query
    