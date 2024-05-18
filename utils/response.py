from typing import Union
from django.http import JsonResponse


def success_response(message: Union[str, None], status=200, **kwargs) -> JsonResponse:
    response = {
        'status': 'success',
    }

    if message is not None:
        response['message'] = message

    response.update(kwargs)

    return JsonResponse(response, status=status)


def error_response(message: Union[str, None], status=300) -> JsonResponse:
    return JsonResponse({
        'status': 'error',
        'message': message,
    }, status=status)
