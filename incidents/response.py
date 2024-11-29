from django.http import JsonResponse

def response_wrapper(data, status_code=200, message="Success"):
    return JsonResponse({
        "status_code": status_code,
        "message": message,
        "data": data,
    })

