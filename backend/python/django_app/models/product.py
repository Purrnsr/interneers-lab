from mongoengine import Document, StringField, FloatField, IntField, BooleanField, DateTimeField
import uuid
from datetime import datetime


class Product(Document):
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))

    name = StringField(required=True)
    description = StringField(required=True)
    category = StringField(required=True)
    brand = StringField(required=True)

    price = FloatField(required=True)
    quantity = IntField(required=True)

    is_deleted = BooleanField(default=False)

    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "products"
    }

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "brand": self.brand,
            "price": self.price,
            "quantity": self.quantity,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }