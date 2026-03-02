from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django_app.controllers.response_utils import success_response, error_response
from django_app.services.product_service import ProductService



@csrf_exempt
def products(request, product_id=None):
    if request.method == "GET":
        if product_id:
            product = ProductService.get_product(product_id)
            if not product:
                return error_response("NOT_FOUND","Product not found", status=404)
            return success_response(product, status=200)

        # Read query params for pagination
        try:
            page = int(request.GET.get("page", 1))
            page_size = int(request.GET.get("page_size", 10))
        except ValueError:
            return JsonResponse({"error": "page and page_size must be integers"}, status=400)

        products = ProductService.list_products(page=page, page_size=page_size)
        return success_response(products,  status=200)

    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return error_response("INVALID_JSON", "Invalid JSON", status=400)


        result = ProductService.create_product(data)

        if "error" in result:
           return error_response("VALIDATION_ERROR", result["error"], status=400)


        return success_response(result, status=201)

    if request.method == "PUT":
        if not product_id:
            return error_response("MISSING_ID", "Product ID required", status=400)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return error_response("INVALID_JSON", "Invalid JSON", status=400)
        
        updated = ProductService.update_product(product_id, data)

        if not updated:
           return error_response("NOT_FOUND", "Product not found", status=404)

        return success_response(updated, status=200)

    if request.method == "DELETE":
        if not product_id:
            return error_response("MISSING_ID", "Product ID required", status=400)

        deleted = ProductService.delete_product(product_id)

        if not deleted:
            return error_response("NOT_FOUND", "Product not found", status=404)

        return success_response(
            {"message": "Product deleted successfully"},
            status=200
        )