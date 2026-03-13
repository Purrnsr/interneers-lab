from mongoengine import Document, StringField, FloatField, IntField, BooleanField, DateTimeField
import uuid
from datetime import datetime
from mongoengine import ReferenceField
from django_app.models.product_category import ProductCategory


class Product(Document):
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))

    name = StringField(required=True)
    description = StringField(required=True)
    category = StringField(required=True)
    brand = StringField(required=True)

    price = FloatField(required=True)
    quantity = IntField(required=True)
    category = ReferenceField(ProductCategory, required=False)
    is_deleted = BooleanField(default=False)
    
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "products"
    }

    def to_dict(self):

        category_id = None

        try:
            if self.category:
                category_id = str(self.category.id)
        except:
            category_id = None

        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "brand": self.brand,
            "price": self.price,
            "quantity": self.quantity,
            "category": category_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }