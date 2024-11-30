from functools import wraps
from django.http import JsonResponse
from incidents.models import Token
from django.utils.timezone import now

def token_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return JsonResponse({
                "status_code": 401,
                "message": "Token not provided",
            }, status=401)
        
        try:
            token_obj = Token.objects.get(token=token)
            request.user = token_obj.user
        except Token.DoesNotExist:
            return JsonResponse({
                "status_code": 401,
                "message": "Invalid token",
            }, status=401)
        
        if token_obj.expiry_date < now():
            token_obj.delete()
            return JsonResponse({
                "status_code": 401,
                "message": "Token expired",
            }, status=401)
        
        return view_func(request, *args, **kwargs)
    
    return wrapper