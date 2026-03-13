import os
import sys

# Add project root (backend/python) to Python path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, BASE_DIR)

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_app.settings")

django.setup()

from django_app.models.product import Product
from django_app.models.product_category import ProductCategory


def run():

    # Create default category if it doesn't exist
    category = ProductCategory.objects(title="General").first()

    if not category:
        category = ProductCategory(
            title="General",
            description="Default category for old products"
        )
        category.save()

    products = Product.objects(category=None)

    updated = 0

    for product in products:
        product.category = category
        product.save()
        updated += 1

    print(f"Updated {updated} products")


if __name__ == "__main__":
    run()