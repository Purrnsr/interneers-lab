from django.http import JsonResponse


def success_response(data=None, status=200):
    return JsonResponse(
        {
            "success": True,
            "data": data
        },
        status=status,
        safe=False
    )


def error_response(code: str, message: str, status=400):
    return JsonResponse(
        {
            "success": False,
            "error": {
                "code": code,
                "message": message
            }
        },
        status=status
    )