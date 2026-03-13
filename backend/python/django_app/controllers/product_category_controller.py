from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from django_app.services.product_category_service import ProductCategoryService
from django_app.controllers.response_utils import success_response, error_response
from django_app.services.product_service import ProductService

@csrf_exempt
def categories(request, category_id=None):

    if request.method == "GET":

        if category_id:
            category = ProductCategoryService.get_category(category_id)

            if not category:
                return error_response("NOT_FOUND", "Category not found", status=404)

            return success_response(category, status=200)

        categories = ProductCategoryService.list_categories()
        return success_response(categories, status=200)


    if request.method == "POST":

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return error_response("INVALID_JSON", "Invalid JSON", status=400)

        result = ProductCategoryService.create_category(data)

        if "error" in result:
            return error_response("VALIDATION_ERROR", result["error"], status=400)

        return success_response(result, status=201)


    if request.method == "PUT":

        if not category_id:
            return error_response("MISSING_ID", "Category ID required", status=400)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return error_response("INVALID_JSON", "Invalid JSON", status=400)

        updated = ProductCategoryService.update_category(category_id, data)

        if not updated:
            return error_response("NOT_FOUND", "Category not found", status=404)

        return success_response(updated, status=200)


    if request.method == "DELETE":

        if not category_id:
            return error_response("MISSING_ID", "Category ID required", status=400)

        deleted = ProductCategoryService.delete_category(category_id)

        if not deleted:
            return error_response("NOT_FOUND", "Category not found", status=404)

        return success_response(
            {"message": "Category deleted successfully"},
            status=200
        )
    
def category_products(request, category_id):

    if request.method != "GET":
        return error_response("METHOD_NOT_ALLOWED", "Only GET allowed", status=405)

    products = ProductService.get_products_by_category(category_id)

    if products is None:
        return error_response("NOT_FOUND", "Category not found", status=404)

    return success_response(products, status=200)
@csrf_exempt
def add_product_to_category(request, category_id, product_id):

    if request.method != "POST":
        return error_response("METHOD_NOT_ALLOWED", "Only POST allowed", status=405)

    result = ProductService.assign_product_to_category(product_id, category_id)

    if result is None:
        return error_response("NOT_FOUND", "Category not found", status=404)

    if result is False:
        return error_response("NOT_FOUND", "Product not found", status=404)

    return success_response(result, status=200)
@csrf_exempt
def remove_product_from_category(request, product_id):

    if request.method != "DELETE":
        return error_response("METHOD_NOT_ALLOWED", "Only DELETE allowed", status=405)

    result = ProductService.remove_product_from_category(product_id)

    if not result:
        return error_response("NOT_FOUND", "Product not found", status=404)

    return success_response(result, status=200)