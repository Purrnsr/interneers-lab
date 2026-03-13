from django_app.models.product_category import ProductCategory


class ProductCategoryRepository:

    @classmethod
    def create(cls, category: ProductCategory):
        category.save()
        return category

    @classmethod
    def get(cls, category_id: str):
        return ProductCategory.objects(id=category_id).first()

    @classmethod
    def list(cls):
        return ProductCategory.objects()

    @classmethod
    def update(cls, category: ProductCategory):
        category.save()
        return category

    @classmethod
    def delete(cls, category_id: str):
        category = ProductCategory.objects(id=category_id).first()
        if not category:
            return False
        category.delete()
        return True