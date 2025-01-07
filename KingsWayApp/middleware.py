# middleware.py
from django.http import HttpResponseForbidden
import re

class SecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/shop/' and request.method == 'POST':
            # Check for suspicious patterns
            if self._is_suspicious(request):
                return HttpResponseForbidden('Request blocked for security reasons.')
        
        response = self.get_response(request)
        return response

    def _is_suspicious(self, request):
        # Check for automated submissions
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        if 'bot' in user_agent or 'crawler' in user_agent or 'spider' in user_agent:
            return True

        # Check for missing or suspicious headers
        if not request.META.get('HTTP_ACCEPT_LANGUAGE'):
            return True

        return False