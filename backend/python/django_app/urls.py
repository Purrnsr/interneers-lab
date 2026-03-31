from django.contrib import admin
from django.urls import path

from django_app.controllers.hello_controller import hello_name
from django_app.controllers.product_controller import products, bulk_upload_products
from django_app.controllers.product_category_controller import (
    categories,
    category_products,
    add_product_to_category,
    remove_product_from_category
)
from django_app.views import product_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello_name),

    path("products/bulk/", bulk_upload_products),

    path('products/', products),
    path('products/<str:product_id>/', products),

    path("categories/", categories),
    path("categories/<str:category_id>/", categories),
    path("categories/<str:category_id>/products/", category_products),
    path("categories/<str:category_id>/products/<str:product_id>/", add_product_to_category),

    path("products/<str:product_id>/remove-category/", remove_product_from_category),
    path("products-page/", product_page)
]