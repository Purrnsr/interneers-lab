from mongoengine import Document, StringField, DateTimeField
import uuid
from datetime import datetime


class ProductCategory(Document):
    id = StringField(primary_key=True, default=lambda: str(uuid.uuid4()))

    title = StringField(required=True, unique=True)
    description = StringField()

    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "product_categories"
    }

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }