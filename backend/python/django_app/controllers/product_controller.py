from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django_app.models.requests.product_request import ProductCreateRequest
from django_app.controllers.response_utils import success_response, error_response
from django_app.services.product_service import ProductService
from django_app.models.responses.product_response import ProductResponse
import csv
from django.views.decorators.csrf import csrf_exempt
from django_app.models.product_category import ProductCategory

@csrf_exempt
def products(request, product_id=None):
    if request.method == "GET":
        if product_id:
            product = ProductService.get_product(product_id)
            if not product:
                return error_response("NOT_FOUND","Product not found", status=404)
            response = ProductResponse(product)
            return success_response(response.to_dict(), status=200)
        updated_after = request.GET.get("updated_after")

        if updated_after:
            products = ProductService.list_products_updated_after(updated_after)
            return success_response(products, status=200)
        category = request.GET.get("category")
        price_min = request.GET.get("price_min")
        price_max = request.GET.get("price_max")

        if category or price_min or price_max:

            price_min = float(price_min) if price_min else None
            price_max = float(price_max) if price_max else None

            products = ProductService.filter_products(
                category=category,
                price_min=price_min,
                price_max=price_max
            )

            return success_response(products, status=200)
        

        # Read query params for pagination
        try:
            page = int(request.GET.get("page", 1))
            page_size = int(request.GET.get("page_size", 10))
        except ValueError:
            return JsonResponse({"error": "page and page_size must be integers"}, status=400)

        products = ProductService.list_products(page=page, page_size=page_size)
        products["data"] = [
            ProductResponse(p).to_dict()
            for p in products["data"]
        ]
        return success_response(products,  status=200)

    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return error_response("INVALID_JSON", "Invalid JSON", status=400)

        # Create request model
        request_model = ProductCreateRequest(data)
        # Validate request
        validation_error = request_model.validate()
        if validation_error:
            return error_response("VALIDATION_ERROR", validation_error["error"], status=400)

        result = ProductService.create_product(data)

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
        if "error" in updated:
            return error_response("VALIDATION_ERROR", updated["error"], status=400)
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


@csrf_exempt
def bulk_upload_products(request):

    if request.method != "POST":
        return error_response("METHOD_NOT_ALLOWED", "Only POST allowed", status=405)

    if "file" not in request.FILES:
        return error_response("NO_FILE", "CSV file required", status=400)

    file = request.FILES["file"]

    decoded = file.read().decode("utf-8").splitlines()
    reader = csv.DictReader(decoded)

    created_products = []
    errors = []

    for row in reader:

        safe_row = dict(row)  # JSON safe copy

        try:
            row["price"] = float(row["price"])
            row["quantity"] = int(row["quantity"])
        except ValueError:
            errors.append({"row": safe_row, "error": "Invalid numeric values"})
            continue

        category_title = row["category"]
        category = ProductCategory.objects(title=category_title).first()

        if not category:
            errors.append({
                "row": safe_row,
                "error": f"Category '{category_title}' not found"
            })
            continue

        row["category"] = category

        result = ProductService.create_product(row)

        if "error" in result:
            errors.append({"row": safe_row, "error": result["error"]})
        else:
            created_products.append(result)

    return success_response(
        {
            "created_count": len(created_products),
            "products": created_products,
            "errors": errors
        },
        status=201
    )