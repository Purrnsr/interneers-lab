from django_app.models.product_category import ProductCategory


def run():

    default_categories = [
        {"title": "Electronics", "description": "Electronic devices"},
        {"title": "Food", "description": "Food products"},
        {"title": "Kitchen Essentials", "description": "Kitchen items"},
        {"title": "General", "description": "Default category"},
    ]

    for category in default_categories:

        existing = ProductCategory.objects(title=category["title"]).first()

        if not existing:
            ProductCategory(
                title=category["title"],
                description=category["description"]
            ).save()

            print(f"Created category: {category['title']}")

        else:
            print(f"Category already exists: {category['title']}")