from django.contrib import admin
from django.urls import path

from django_app.controllers.hello_controller import hello_name
from django_app.controllers.product_controller import products
from django_app.controllers.product_category_controller import categories
from django_app.controllers.product_category_controller import category_products
from django_app.controllers.product_category_controller import (
    add_product_to_category,
    remove_product_from_category
)
from django_app.controllers.product_controller import bulk_upload_products

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello_name),

    # BULK upload first (specific route)
    path("products/bulk/", bulk_upload_products),

    # RESTful Product endpoints
    path('products/', products),
    path('products/<str:product_id>/', products),

    path("categories/", categories),
    path("categories/<str:category_id>/", categories),
    path("categories/<str:category_id>/products/", category_products),
    path("categories/<str:category_id>/products/<str:product_id>/", add_product_to_category),

    path("products/<str:product_id>/remove-category/", remove_product_from_category),
]

