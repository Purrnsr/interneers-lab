from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from django_app.services.product_service import ProductService



@csrf_exempt
def products(request, product_id=None):
    if request.method == "GET":
        if product_id:
            product = ProductService.get_product(product_id)
            if not product:
                return JsonResponse({"error": "Product not found"}, status=404)
            return JsonResponse(product, status=200)

        products = ProductService.list_products()
        return JsonResponse(products, safe=False, status=200)

    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        result = ProductService.create_product(data)

        if "error" in result:
            return JsonResponse(result, status=400)

        return JsonResponse(result, status=201)

    if request.method == "PUT":
        if not product_id:
            return JsonResponse({"error": "Product ID required"}, status=400)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        updated = ProductService.update_product(product_id, data)

        if not updated:
            return JsonResponse({"error": "Product not found"}, status=404)

        return JsonResponse(updated, status=200)

    if request.method == "DELETE":
        if not product_id:
            return JsonResponse({"error": "Product ID required"}, status=400)

        deleted = ProductService.delete_product(product_id)

        if not deleted:
            return JsonResponse({"error": "Product not found"}, status=404)

        return JsonResponse({"message": "Product deleted successfully"}, status=200)

    return JsonResponse({"error": "Method not allowed"}, status=405)