from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

from django_app.services.product_service import ProductService


@csrf_exempt
@require_http_methods(["POST"])
def create_product(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    result = ProductService.create_product(data)

    if "error" in result:
        return JsonResponse(result, status=400)

    return JsonResponse(result, status=201)


@require_http_methods(["GET"])
def list_products(request):
    products = ProductService.list_products()
    return JsonResponse(products, safe=False, status=200)


@require_http_methods(["GET"])
def get_product(request, product_id):
    product = ProductService.get_product(product_id)

    if not product:
        return JsonResponse({"error": "Product not found"}, status=404)

    return JsonResponse(product, status=200)


@csrf_exempt
@require_http_methods(["PUT"])
def update_product(request, product_id):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    updated_product = ProductService.update_product(product_id, data)

    if not updated_product:
        return JsonResponse({"error": "Product not found"}, status=404)

    return JsonResponse(updated_product, status=200)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_product(request, product_id):
    deleted = ProductService.delete_product(product_id)

    if not deleted:
        return JsonResponse({"error": "Product not found"}, status=404)

    return JsonResponse({"message": "Product deleted successfully"}, status=200)