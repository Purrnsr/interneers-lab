from django_app.models.product import Product
from django_app.repositories.product_repository import ProductRepository
from typing import Dict, List
from django_app.repositories.product_category_repository import ProductCategoryRepository
from django_app.models.product_category import ProductCategory
from django_app.utils.logger import logger


class ProductService:
    repository = ProductRepository
    category_repository = ProductCategoryRepository

    @classmethod
    def create_product(cls, data: dict) -> dict:

        logger.info("Creating product")

        #  VALIDATION FIRST (NO try-catch)
        required_fields = ["name", "description", "category", "price", "brand", "quantity"]

        for field in required_fields:
            if field not in data:
             return {"error": f"{field} is required"}

        if not isinstance(data["brand"], str) or not data["brand"].strip():
            return {"error": "brand must be a non-empty string"}

        if not isinstance(data["name"], str) or not data["name"].strip():
            return {"error": "name must be a non-empty string"}

        if not isinstance(data["description"], str) or not data["description"].strip():
            return {"error": "description must be a non-empty string"}

        if not isinstance(data["price"], (int, float)) or data["price"] <= 0:
            return {"error": "price must be a positive number"}

        if not isinstance(data["quantity"], int) or data["quantity"] < 0:
            return {"error": "quantity must be a non-negative integer"}

        #  category handling (both test + API)
        category = data.get("category")

        if isinstance(category, ProductCategory):
            pass
        else:
            category = cls.category_repository.get(category)
            if not category:
                return {"error": "invalid category"}

        data["category"] = category

        #  ONLY DB LOGIC INSIDE try
        try:
            product = Product(
                name=data["name"].strip(),
                description=data["description"].strip(),
                category=data["category"],
                price=data["price"],
                brand=data["brand"].strip(),
                quantity=data["quantity"],
            )

            cls.repository.create(product)

            return product.to_dict()

        except Exception as e:
            logger.error(f"Error creating product: {str(e)}")
            return {"error": "Internal server error"}
    
    @classmethod
    def get_product(cls, product_id: str) -> dict:
        product = cls.repository.get(product_id)
        if not product or product.is_deleted:
            return None
        return product.to_dict()

    @classmethod
    def list_products(cls, page: int = 1, page_size: int = 10) -> dict:
        active_products = [
            product.to_dict()
            for product in cls.repository.list()
            if not product.is_deleted
        ]

        total_items = len(active_products)
        total_pages = (total_items + page_size - 1) // page_size

        start = (page - 1) * page_size
        end = start + page_size

        return {
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages,
            "data": active_products[start:end],
        }

    @classmethod
    def update_product(cls, product_id: str, data: dict) -> dict:
        try:
            product = cls.repository.get(product_id)

            if not product or product.is_deleted:
                return None

            if "name" in data:
                if not isinstance(data["name"], str) or not data["name"].strip():
                    return {"error": "name must be a non-empty string"}
                product.name = data["name"].strip()

            if "description" in data:
                if not isinstance(data["description"], str) or not data["description"].strip():
                    return {"error": "description must be a non-empty string"}
                product.description = data["description"].strip()

            if "brand" in data:
                if not isinstance(data["brand"], str) or not data["brand"].strip():
                    return {"error": "brand must be a non-empty string"}
                product.brand = data["brand"].strip()

            if "price" in data:
                if not isinstance(data["price"], (int, float)) or data["price"] <= 0:
                    return {"error": "price must be a positive number"}
                product.price = data["price"]

            if "quantity" in data:
                if not isinstance(data["quantity"], int) or data["quantity"] < 0:
                    return {"error": "quantity must be a non-negative integer"}
                product.quantity = data["quantity"]

            if "category" in data:
                category = cls.category_repository.get(data["category"])
                if not category:
                    return {"error": "invalid category"}
                product.category = category

            cls.repository.update(product)

            return product.to_dict()

        except Exception as e:
            logger.error(f"Error updating product: {str(e)}")
            return {"error": "Internal server error"}

    @classmethod
    def delete_product(cls, product_id: str):
        deleted = cls.repository.delete(product_id)
        if not deleted:
            return None
        return {"message": "Product deleted successfully"}

    @classmethod
    def list_products_updated_after(cls, timestamp: str):
        products = cls.repository.list_updated_after(timestamp)
        return [product.to_dict() for product in products]

    @classmethod
    def get_products_by_category(cls, category_id: str):
        products = cls.repository.get_products_by_category(category_id)
        if products is None:
            return None
        return [p.to_dict() for p in products]

    @classmethod
    def assign_product_to_category(cls, product_id: str, category_id: str):
        category = cls.category_repository.get(category_id)
        if not category:
            return None

        product = cls.repository.assign_category(product_id, category)
        if not product:
            return False

        return product.to_dict()

    @classmethod
    def remove_product_from_category(cls, product_id: str):
        product = cls.repository.remove_category(product_id)
        if not product:
            return None
        return product.to_dict()

    @classmethod
    def filter_products(cls, category=None, price_min=None, price_max=None):
        category_titles = None

        if category:
            category_titles = [c.strip() for c in category.split(",")]

        products = cls.repository.filter_products(
            category_titles=category_titles,
            price_min=price_min,
            price_max=price_max
        )

        return [p.to_dict() for p in products]

    @classmethod
    def bulk_create_products(cls, file) -> dict:
        import csv

        try:
            logger.info("Starting bulk product upload")

            decoded = file.read().decode("utf-8").splitlines()
            reader = csv.DictReader(decoded)

            created_products = []
            errors = []

            for row in reader:
                safe_row = dict(row)

                # Numeric validation
                try:
                    row["price"] = float(row["price"])
                    row["quantity"] = int(row["quantity"])
                except:
                    errors.append({
                        "row": safe_row,
                        "error": "Invalid price or quantity"
                    })
                    continue

                #  Category validation (USE REPOSITORY)
                category_title = row.get("category")

                category = cls.category_repository.list().filter(
                    title=category_title
                ).first()

                if not category:
                    errors.append({
                        "row": safe_row,
                        "error": "Invalid category"
                    })
                    continue  #  IMPORTANT

                row["category"] = category

                # Create product
                result = cls.create_product(row)

                if "error" in result:
                    errors.append({
                        "row":safe_row,
                        "error": result["error"]
                    })
                else:
                    created_products.append(result)

            # Always return structured response
            return {
                "created_count": len(created_products),
                "products": created_products,
                "errors": errors
            }

        except Exception as e:
            logger.error(f"Bulk upload failed: {str(e)}")
            return {"error": "Internal server error"}