from django.core.management.base import BaseCommand
from django_app.models.product_category import ProductCategory
from django_app.utils.logger import logger


class Command(BaseCommand):
    help = "Seed default product categories"

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete existing categories before seeding",
        )

    def handle(self, *args, **options):
        if options["reset"]:
            ProductCategory.objects.delete()
            self.stdout.write(self.style.WARNING("Existing categories deleted"))

        categories = [
            {"title": "Electronics", "description": "Electronic items"},
            {"title": "Food", "description": "Food items"},
            {"title": "Kitchen Essentials", "description": "Kitchen items"},
            {"title": "General", "description": "General items"},
        ]

        for cat in categories:
            existing = ProductCategory.objects(title=cat["title"]).first()

            if existing:
                self.stdout.write(self.style.WARNING(f"Already exists: {cat['title']}"))
            else:
                ProductCategory(**cat).save()
                self.stdout.write(self.style.SUCCESS(f"Created: {cat['title']}"))

        logger.info("Category seeding completed")
        self.stdout.write(self.style.SUCCESS("Seeding complete"))