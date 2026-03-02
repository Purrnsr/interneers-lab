from django.contrib import admin
from django.urls import path

from django_app.controllers.hello_controller import hello_name
from django_app.controllers.product_controller import products

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', hello_name),

    # RESTful Product endpoints
    path('products/', products),
    path('products/<str:product_id>/', products),
]

