import uuid


class Product:
    def __init__(self, name, description, category, price, brand, quantity):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.category = category
        self.price = price
        self.brand = brand
        self.quantity = quantity
        self.is_deleted = False

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