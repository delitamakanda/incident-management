from django.http import HttpResponseForbidden
from django.core.cache import cache

class DDosMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.time_window = 60  # seconds
        self.requests_limit = 1000  # requests per time window
        
    def process_request(self, request):
        ip_address = request.META.get('REMOTE_ADDR')
        cache_key = f"ddos_requests_{ip_address}"
        
        current_requests = cache.get(cache_key, 0)
        if current_requests >= self.requests_limit:
            return HttpResponseForbidden("Too many requests, please try again later.")
        
        cache.set(cache_key, current_requests + 1, self.time_window)
        return None
    
    def __call__(self, request):
        return self.process_request(request) or self.get_response(request)
        