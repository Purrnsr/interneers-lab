from django.http import JsonResponse
from django.views.decorators.http import require_GET

from django_app.services.hello_service import HelloService


@require_GET
def hello_name(request):
    """
    Controller layer.
    Handles HTTP request and delegates business logic to service.
    """

    # Extract query parameter
    name = request.GET.get("name", "")

    # Call service layer
    response_data = HelloService.generate_greeting(name)

    # Determine HTTP status
    if "error" in response_data:
        return JsonResponse(response_data, status=400)

    return JsonResponse(response_data, status=200)
