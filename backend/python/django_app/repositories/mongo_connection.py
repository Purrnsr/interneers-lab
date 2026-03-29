from mongoengine import connect
from django.conf import settings


def init_db():
    if not settings.MONGO_URI:
        raise Exception("MONGO_URI not set")

    connect(host=settings.MONGO_URI)