class ProductResponse:
    """
    Response model for Product API responses.
    Ensures consistent output structure.
    """

    def __init__(self, product: dict):
        self.id = product.get("id")
        self.name = product.get("name")
        self.description = product.get("description")
        self.category = product.get("category")
        self.price = product.get("price")
        self.brand = product.get("brand")
        self.quantity = product.get("quantity")

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