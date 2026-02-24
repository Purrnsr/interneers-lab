from django.contrib import admin
from django.urls import path

from django_app.controllers.hello_controller import hello_name
from django_app.controllers.product_controller import (
    create_product,
    list_products,
    get_product,
    update_product,
    delete_product,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Hello endpoint
    path('hello/', hello_name),

    # Product endpoints
    path('products/', create_product),          # POST
    path('products/list/', list_products),      # GET (list)
    path('products/<str:product_id>/', get_product),  # GET (single)
    path('products/<str:product_id>/update/', update_product),  # PUT
    path('products/<str:product_id>/delete/', delete_product),  # DELETE
]