from django.apps import AppConfig
from django_app.repositories.mongo_connection import init_db


class DjangoAppConfig(AppConfig):
    name = "django_app"

    def ready(self):
        init_db()