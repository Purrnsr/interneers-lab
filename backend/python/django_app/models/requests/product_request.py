class ProductCreateRequest:
    """
    Request model for creating a product.
    Responsible for validating incoming API data.
    """

    def __init__(self, data: dict):
        self.name = data.get("name")
        self.description = data.get("description")
        self.category = data.get("category")
        self.price = data.get("price")
        self.brand = data.get("brand")
        self.quantity = data.get("quantity")

    def validate(self):
        required_fields = [
            "name",
            "description",
            "category",
            "price",
            "brand",
            "quantity",
        ]

        for field in required_fields:
            value = getattr(self, field)
            if value is None:
                return {"error": f"{field} is required"}

        if not isinstance(self.name, str) or not self.name.strip():
            return {"error": "name must be a non-empty string"}

        if not isinstance(self.description, str) or not self.description.strip():
            return {"error": "description must be a non-empty string"}

        if not isinstance(self.category, str) or not self.category.strip():
            return {"error": "category must be a non-empty string"}

        if not isinstance(self.brand, str) or not self.brand.strip():
            return {"error": "brand must be a non-empty string"}

        if not isinstance(self.price, (int, float)) or self.price <= 0:
            return {"error": "price must be a positive number"}

        if not isinstance(self.quantity, int) or self.quantity < 0:
            return {"error": "quantity must be a non-negative integer"}

        return None